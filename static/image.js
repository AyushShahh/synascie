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

var node = document.getElementById('art');
var scale = 4;

document.getElementById("save").addEventListener('click', () => {
    domtoimage.toJpeg(art, {
        width: art.clientWidth * scale,
        height: art.clientHeight * scale,
        quality: 1,
        style: {
            transform: 'scale('+scale+')',
            transformOrigin: 'top left'
        }})
        .then(function (dataUrl) {
            var link = document.createElement('a');
            link.download = 'ascii.jpeg';
            link.href = dataUrl;
            link.click();
        });
})