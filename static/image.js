// document.querySelectorAll('.background').forEach(item => {
//     const art = document.querySelector(".art");
//     item.addEventListener('click', event => {
//         art.style.background = item.value;
//         if (item.value == "white")
//         {
//             art.style.color = "black";
//         }
//         else
//         {
//             art.style.color = "white";
//         }
//     })
// })

// Get node, button and set scale
var node = document.getElementById('art');
var button = document.getElementById('save');

// Add event listener and use dom-to-image to convert div to canvas
button.addEventListener('click', () => {
    button.disabled = true;
    button.innerText = "Generating...";
    var nodeClone = node.cloneNode(true);
    html2canvas(nodeClone, {
        scale: 5, // set the scale factor to 5
        backgroundColor: null, // set background color to transparent
      }).then(function(canvas) {
        // convert canvas to data URL and download as JPEG
        var link = document.createElement("a");
        link.download = "ascii.jpg";
        link.href = canvas.toDataURL("image/jpeg", 1.0);
        link.click();
        button.disabled = false;
        button.innerText = "Save as jpeg";
      }
    ); 
});