document.getElementById('browser-resolution').value = screen.width + "x" + screen.height;

function getAndPostSize(event) {
  const file = event.target.files[0];
  if (file) {
    const fileSize = file.size; // in bytes
    document.getElementById('size').value = fileSize;
    if (fileSize > 4.5 * 1024 * 1024) 
    {
      document.getElementById("file").remove();
      document.getElementById("form").submit();
    }
  }
}

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