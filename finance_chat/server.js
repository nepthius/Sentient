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
      /*
      else if(test == 2){
        (async () => {
            const response = await cohere.classify({
              model: '489cf173-a605-4ed6-9a90-67a97244673f-ft',
              inputs: [msg]
            });
            io.emit('chat message', (`Chatbot: Your statement is perceived as ${((response.body.classifications)[0]).prediction}`));
          })();
      }
      */
    });
});
