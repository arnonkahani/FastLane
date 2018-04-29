function clickWrapper(button){
    
    
    button.addEventListener('click',function(args){
        
        let data = {
            url: document.URL,
            buttonId: button.id
        }
        console.log(data)
        axios.post('/analytics', data)

    })
}

window.Einav = {name:"Einav",clickWrapper:clickWrapper}

// html2canvas(document.body).then(function (canvas) {
//     document.getElementById("capture").appendChild(canvas);
//     document.onmousemove = function (event) {
//         var x = event.clientX * (document.getElementById("capture").childNodes[0].width / document.documentElement.scrollWidth);
//         var y = event.clientY * (document.getElementById("capture").childNodes[0].height / document.documentElement.scrollHeight);
//         var coor = "X coords: " + x + ", Y coords: " + y;
//         var canvas = document.getElementById("capture").childNodes[0];
//         var ctx = canvas.getContext('2d');
//         ctx.fillStyle = 'rgba(0, 0, 200, 0.1)';
//         ctx.fillRect(x, y, 5, 5);
//     }


// });