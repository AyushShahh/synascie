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
var scale = 5;
var button = document.getElementById('save');

// Add event listener and use dom-to-image to convert div to canvas
button.addEventListener('click', () => {
    button.disabled = true;
    button.innerText = "Generating...";
    node.style.width = node.clientWidth * scale + 'px';
    node.style.height = node.clientHeight * scale + 'px';
    domtoimage.toJpeg(node, {
        // increase width by scale
        width: node.style.width,
        height: node.style.height,
        quality: 1,
        })
        // convert canvas to dataurl & create and click link to download image
        .then(function (dataUrl) {
            var link = document.createElement('a');
            link.download = 'ascii.jpeg';
            link.href = dataUrl;
            link.click();
            button.disabled = false;
            button.innerText = "Save as jpeg";
        }
    );
});