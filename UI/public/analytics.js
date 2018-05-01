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

function log_movment(document){


window.log_movment_data = []

document.onmousemove = function(event){
     var x = event.clientX;
     var y = event.clientY;
     window.log_movment_data.push([x,y])
     }


setInterval(function(){
 let data = {
            url: document.URL,
            movment_data: window.log_movment_data
        }
        console.log(data)

        axios.post('/analytics/movment', data)
        window.log_movment_data = []


 }, 5000);

}

window.Einav = {name:"Einav",clickWrapper:clickWrapper,log_movment:log_movment}

