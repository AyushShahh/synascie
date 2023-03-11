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

$(function() { 
    $("#save").click(function() { 
        html2canvas($("#art"), {
            onrendered: function(canvas) {
                theCanvas = canvas;
                canvas.toBlob(function(blob) {
                    saveAs(blob, "ascii.png");
                });
            }
        });
    });
});  