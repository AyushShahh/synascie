if(navigator.userAgent.includes("Instagram") || navigator.userAgent.includes("FBAV"))
{
  if (document.referrer != "https://openinapp.co/" && !(/iPad|iPhone|iPod/.test(navigator.userAgent)))
  {
    window.location.replace('https://openinapp.co/ascii');
  }
}

else {
  // Get user's device screen width and height
  document.getElementById('browser-resolution').value = screen.width + "x" + screen.height;

  // Remove prev file on input
  // var fileInp = document.getElementById("file");
  // fileInp.addEventListener("click", () => {
  //   fileInp.value = "";
  // });

  // Get size of image and set its value and preview for rotation
  function getAndPostSize(event) {
    const file = event.target.files[0];
    if (file) {
      const fileSize = file.size; // in bytes
      document.getElementById('size').value = fileSize;
      // If greater than 4.5 MB, remove image file and submit form
      if (fileSize > 4.5 * 1024 * 1024) 
      {
        event.target.value = '';
        document.getElementById("form").submit();
      }
      else if (file.type.startsWith('image/'))
      {
        var angleInput = document.getElementById("rotate");
        var angle = parseInt(angleInput.value);
        var button = document.getElementById("sub");
        button.disabled = true;
        // Read the Exif Orientation information
        EXIF.getData(file, function() {
          var orientation = EXIF.getTag(this, "Orientation");
          
          // Create a new FileReader instance
          var reader = new FileReader();
          
          // When the file is loaded, set the image source and rotate based on the orientation
          reader.onload = function(event) {
            var img = new Image();
            img.src = event.target.result;
            
            img.onload = function() {
              var canvas = document.createElement('canvas');
              var ctx = canvas.getContext('2d');
              var width = img.width;
              var height = img.height;
              
              if (orientation > 4 && orientation < 9) {
                canvas.width = height;
                canvas.height = width;
              } else {
                canvas.width = width;
                canvas.height = height;
              }
              
              switch (orientation) {
                case 2:
                  ctx.transform(-1, 0, 0, 1, width, 0);
                  break;
                case 3:
                  ctx.transform(-1, 0, 0, -1, width, height);
                  break;
                case 4:
                  ctx.transform(1, 0, 0, -1, 0, height);
                  break;
                case 5:
                  ctx.transform(0, 1, 1, 0, 0, 0);
                  break;
                case 6:
                  ctx.transform(0, -1, 1, 0, 0, width);
                  break;
                case 7:
                  ctx.transform(0, -1, -1, 0, height, width);
                  break;
                case 8:
                  ctx.transform(0, 1, -1, 0, height, 0);
                  break;
                default:
                  ctx.transform(1, 0, 0, 1, 0, 0);
                  break;
              }
              
              ctx.drawImage(img, 0, 0);
              var rotatedDataUrl = canvas.toDataURL('image/jpeg', 0.85);
              var container = $('<div>').css({
                background: 'RGBA(0,0,0,.5)',
                backgroundSize: 'contain',
                width: '100%',
                height: '100%',
                position: 'fixed',
                zIndex: '10000',
                top: '0',
                left: '0'
              }).appendTo('body');
              var modal = $('<div>').css({
                'background-image': 'url(' + rotatedDataUrl + ')',
                'background-repeat': 'no-repeat',
                'background-position': 'center',
                'background-size': 'cover',
                'image-orientation': 'from-image',
                backgroundSize: 'contain',
                width: '90%',
                height: '90%',
                position: 'fixed',
                zIndex: '10010',
                top: '5%',
                left: '5%',
                transition: 'transform 0.5s ease'
              });
              var buttoncontainer = $('<div class="align">').css({
                width: '100%',
                bottom: '5%',
                position: 'fixed',
                zIndex: '10020'
              })
              var rot = $('<button class="button">').html('Rotate &#8634;').click(function() {
                angle += 90;
                angleInput.value = angle % 360;
                modal.css({
                  transform: 'rotate(-'+ angle + 'deg)'
                })
              }).appendTo(buttoncontainer);
              var done = $('<button class="button">').text('Done').click(function () {
                container.remove();
              }).appendTo(buttoncontainer);
              rot.add(done).css("border-color", "white");
              container.append(modal, buttoncontainer);
            }
          };
          // Read the file as a data URL
          reader.readAsDataURL(file);
        })
        button.disabled = false;
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