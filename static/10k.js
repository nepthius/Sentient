const waiting = document.getElementById("waiting");
const resultTable = document.getElementById("result-table");
waiting.style.display = "none";
// resultTable.style.display = "none";

$("#submit").click(function (e) {
    e.preventDefault();
    const sticker = document.getElementById("text-input").value;
    console.log(sticker);
    waiting.style.display = "block";

    setTimeout(() => {
        waiting.style.display = "none";
        // show table html here
        // resultTable.classList.remove("hidden");
        resultTable.style.display = "flex";
        $("#result").html("Input sticker is: " + sticker);
        }, 1000);

    $.post( "/10k-analysis", {
        javascript_data: sticker
    });

    
});





$('input[type="file"]').change( function (e) {
    //read data from file upload
    // console.log(e.target.files[0]);
    let reader = new FileReader();
    // trigger filereader onload
    reader.readAsDataURL(e.target.files[0]);
    reader.onload = function (event) {
        let thisData = event.target.result;
        // console.log(thisData);
        let userUploadJSON = JSON.stringify(thisData);
        localStorage.setItem("fileData", userUploadJSON);
        console.log(userUploadJSON);
    };

});

$(document).ready(function(){
    $("a").on('click', function(event) {
      if (this.hash !== "") {
        event.preventDefault();
        var hash = this.hash;
        $('body,html').animate({
        scrollTop: $(hash).offset().top
        }, 1200, function(){
        window.location.hash = hash;
       });
       } 
      });
    
      // expand clicking area
      const uploadFileform = document.querySelector("#upload-area");
      fileInput = document.querySelector(".file-input");
      // form click event
      uploadFileform.addEventListener("click", () =>{
        fileInput.click();
        });
  });
  
  var width = $(window).width(); 
  
  window.onscroll = function(){
  if ((width >= 900)){
      if(document.body.scrollTop > 80 || document.documentElement.scrollTop > 80) {
          $("#middle").css("background-size","150% auto");
      }else{
          $("#middle").css("background-size","100% auto");        
      }
  }
  };
  
  setTimeout(function(){
      $("#loading").addClass("animated fadeOut");
      setTimeout(function(){
        $("#loading").removeClass("animated fadeOut");
        $("#loading").css("display","none");
      },800);
  },1450);