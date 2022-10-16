
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
      const form = document.querySelector("form");
      fileInput = document.querySelector(".file-input");
      // form click event
      form.addEventListener("click", () =>{
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