function clickWrapper(button,uuid){
    
    console.log("senging click")
    button.addEventListener('click',function(args){

         let data = {
            event_url: document.URL,
            event_uuid: window.uuid,
            event_type: 'button_click',
            event_data: {
            x:args.clientX,
            y:args.clientY,
            id:button.id
            }
        }
        console.log("senging click")
        axios.post('/analytics', data)

    })
}

function log_movment(document,uuid){


window.log_movment_data = []

document.onmousemove = function(event){
     var x = event.clientX;
     var y = event.clientY;
     window.log_movment_data.push([x,y])
     window.uuid = uuid
     }


setInterval(function(){
 let data = {
            event_url: document.URL,
            event_type: 'movement',
            event_data: window.log_movment_data,
            event_uuid: window.uuid
        }
        console.log(data)
        axios.post('/analytics', data)
        window.log_movment_data = []
 }, 5000);

}

window.analytics_handlers = {clickWrapper:clickWrapper,log_movment:log_movment}

