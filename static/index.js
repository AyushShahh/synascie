if(navigator.userAgent.includes("Instagram"))
{
  document.querySelector('.upload').innerHTML = "<h2 style='text-decoration:line-through black 3px'>Upload an image</h2><p class='orange' style='font-size:smaller; word-break: normal'><b>You are currently using Instagram's in-app browser</b></p><p style='word-break: normal'>Instagram's in-app browser has a lot of limitations and lesser features so this site does not work on on this browser.<br><br>Kindly open this site in your mobile's native browser (chrome/safari/etc) by clicking on the three dots &nbsp;<b style='font-size:larger'>&#8942;</b>&nbsp; in the top right corner or,<br><br>click on <b id='txt' style='color:lightskyblue; text-decoration:underline'>https://asciiiart.vercel.app/</b> this link to copy and then head over to your mobile's native browser and paste it to open this site.</p><p class='orange' id='copy' style='font-size:smaller; text-align:center'></p>";

  $("#txt").on("click", function (event) {
    var $temp = $("<input>");
    $("body").append($temp);
    $temp.val($("#txt").html()).select();
    document.execCommand("copy");
    $temp.remove();
    $("#copy").html("Link copied!");
  });
}

else {
  // Get user's device screen width and height
  document.getElementById('browser-resolution').value = screen.width + "x" + screen.height;

  // Get size of image and set its value
  function getAndPostSize(event) {
    const file = event.target.files[0];
    if (file) {
      const fileSize = file.size; // in bytes
      document.getElementById('size').value = fileSize;
      // If greater than 4.5 MB, remove image file and submit form
      if (fileSize > 4.5 * 1024 * 1024) 
      {
        document.getElementById("file").remove();
        document.getElementById("form").submit();
      }
    }
  }
}

// Clicking on image will enlarge it fullscreen with high z-index
$('img[data-enlargeable]').addClass('img-enlargeable').click(function() {
    var src = $(this).attr('src');
    var modal;
  
    function removeModal() {
      modal.remove();
      $('body').off('keyup.modal-close');
    }
    modal = $('<div>').css({
      background: 'RGBA(0,0,0,.5) url(' + src + ') no-repeat center',
      backgroundSize: 'contain',
      width: '100%',
      height: '100%',
      position: 'fixed',
      zIndex: '10000',
      top: '0',
      left: '0',
      cursor: 'zoom-out'
    }).click(function() {
      removeModal();
    }).appendTo('body');
    //handling ESC
    $('body').on('keyup.modal-close', function(e) {
      if (e.key === 'Escape') {
        removeModal();
      }
    });
    // handling back button on mobile
    if (window.history && window.history.pushState) {
        window.history.pushState('forward', null, './');
        $(window).on('popstate', function() {
            removeModal();
        });
      }
  });