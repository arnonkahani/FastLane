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

{/* <a id="demo"></a> */}


// document.onmousemove = function(event){
//     var x = event.clientX;
//     var y = event.clientY; 
//     var coor = "X coords: " + x + ", Y coords: " + y;
//     document.getElementById("demo").innerHTML = coor;
//     }