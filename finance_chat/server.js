const express = require('express');
const app = express();
const dotenv = require("dotenv");
dotenv.config()
const http = require('http');
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server);
const cohere = require('cohere-ai');
cohere.init(process.env.API);


//Stores whether it is generating or classifying
let test = 0

//connect to CockroachDB
server.listen(3000)


//register view engine 
app.set('view engine', 'ejs');

secret: process.env.SESSION_SECRET

app.get('/', (req,res) => {
    test = 1
    res.render('generate.ejs')
})

app.get('/classify', (req,res) => {
    test = 2
    res.render('classify.ejs')
})

//Stores prompt
p = 'Question: How do I stay focused?\nAnswer: Eliminate distractions \n--\nQuestion: How do I eat less?\nAnswer: Drink more water.\n--\nQuestion: How can I stay calm?\nAnswer: Take deep breaths.\n--\nQuestion: How to become less hungry?\nAnswer: Don\'t eat too much.\n--\nQuestion: How to stay happy?\nAnswer: Eat more.\n--\n'

io.on('connection', (socket) => {
    socket.on('chat message', (msg) => {
      const username = "You"
      console.log(username)
      io.emit('chat message', (username + ': ' + msg));
      console.log(test)

      //Generates chatbot text to talk to user
      if(test == 1){
        p += `Question: ${msg}` + '\nAnswer: ';
        console.log(p);
        (async () => {
            const response = await cohere.generate({
                model: 'small',
                prompt: p,
                max_tokens: 50,
                temperature: 0.9,
                k: 0,
                p: 0.75,
                frequency_penalty: 0,
                presence_penalty: 0,
                stop_sequences: ["--"],
                return_likelihoods: 'NONE'
            });
            s = `${response.body.generations[0].text}`
            s = s.split("--")
            for(let i = 0; i < s.length; i++){
                console.log("String piece:" + s[i])
                if(s[i].includes('Question:') || s[i].includes('Answer:') || s[i].includes('                           ')){
                    console.log("it has a question or answer")
                    break
                }
                else{
                    if(s != '\n' || s != '' || s!=null){
                        io.emit('chat message', ("Chatbot: " + s[i]))
                        p += s[i]
                    }
            }
            p+= '\n--\n'
            
            }
            
        })();
      }
      
      else if(test == 2){
        (async () => {
            const response = await cohere.classify({
              model: 'large',
              inputs: [msg],
              examples: [{"text": "High interest rates", "label": "Negative"}, {"text": "The economy is falling apart", "label": "Negative"}, {"text": "The economy is doing well", "label": "Positive"}, {"text": "The economy is going down", "label": "Negative"}, {"text": "Low interest rates", "label": "Positive"}, {"text": "GDP is down", "label": "Negative"}, {"text": "GDP is up", "label": "Positive"}, {"text": "High debt", "label": "Negative"}, {"text": "Low debt", "label": "Positive"}, {"text": "Inflation is high", "label": "Negative"}, {"text": "Inflation is low", "label": "Positive"}, {"text": "There is a recession", "label": "Negative"}, {"text": "Recession", "label": "Negative"}, {"text": "Crash", "label": "Negative"}] 
            });
            io.emit('chat message', (`Chatbot: Your statement is perceived as ${((response.body.classifications)[0]).prediction}`));
          })();
      }
      
    });

});
