function clickWrapper(button){
    
    
    button.addEventListener('click',function(args){
        
        let data = {
            url: document.URL,
            buttonId: button.id
        }
         let data = {
            event_url: document.URL,
            event_type: 'button_click',
            event_data: {
            x:e.clientX,
            y:e.clientY,
            id:button.id
            }
        }
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

