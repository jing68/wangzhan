
var num = []
var op = []
var all_num = []
var i = 0
var co = true;
function dis(val)
{       
    //get current display number and convert to integer
    var display = document.getElementById("calc-display").value;
    var newdisplay = parseInt(display)  //newdisplay is 0 at first
    switch (val) {
        case 'add':   
            if (i==1) {
                op.push('+')
                num = []
                co = false              
                break;
            } 
            else {      
                op.push('+')
                console.log('op: '+op);                   
                num = []
                all_num.push(newdisplay)          
                console.log('all_num: '+all_num)          
                co = true
                i = 1
                break;
            }
        case 'minus':
            if (i==1){
                op.push('-')
                num = []
                co=false            
                break;
            }
            else { 
                op.push('-')
                //all_num_op.push('-')
                console.log(op);         
                num = []
                all_num.push(newdisplay)
                console.log(all_num)
                co = true
                i = 1
                break;
            }
        case 'time':
            if (i ==1){
                op.push('*')
                num = []
                co=false
                break;
            }
            else {
                op.push('*')
                //all_num_op.push('*')
                console.log(op);        
                num = []
                all_num.push(newdisplay)
                console.log(all_num)
                co = true  
                i=1         
                break;
            }
        case 'divide':
            if (i==1){
                op.push('/')
                num = []
                co=false
                break;
            }
            else {
                op.push('/')
                console.log(op)          
                num = []
                all_num.push(newdisplay)
                console.log(all_num)
                co = true  
                i=1        
                break;
            }
        case 'equal':
            op.push('=')
            console.log(op)
            num = []
            all_num.push(newdisplay)
            console.log(all_num)
            co = true
            break;
        default:
            if(newdisplay == 0) {
                var result = parseInt(val) + newdisplay
                document.getElementById("calc-display").value = result
                num.push(val)
                newdisplay = document.getElementById("calc-display").value
                newdisplay = parseInt(newdisplay)
                console.log('num: '+num)
                console.log('newdisplay: '+newdisplay) 
                i=0                               
                co = false;             
            }
            else if(newdisplay != 0){  
                //all_num.push(newdisplay)           
                num.push(val)             
                console.log('num: '+ num)
                console.log('all_num: '+all_num)
                document.getElementById("calc-display").value = num.join("")
                newdisplay = document.getElementById("calc-display").value               
                newdisplay = parseInt(newdisplay) 
                console.log('newdisplay:'+newdisplay) 
                i=0                      
                co = false;               
            }
    }
    if (op.length>1 && co == true) {
        
        
        if (op[op.length-2]=='+') {
            addition = all_num[all_num.length-2]+all_num[all_num.length-1]
            console.log(addition)
            document.getElementById("calc-display").value = addition
            newdisplay = parseInt(document.getElementById("calc-display").value)
            console.log(newdisplay)
            all_num.push(newdisplay)
            console.log(all_num)
        }
        else if (op[op.length-2]=='-') {
            console.log("hhh")
            sub = all_num[all_num.length-2] - all_num[all_num.length-1]
            console.log(sub)
            document.getElementById("calc-display").value = sub
            newdisplay = parseInt(document.getElementById("calc-display").value)
            console.log(newdisplay)
            all_num.push(newdisplay)
            console.log(all_num)
        }
        else if (op[op.length-2]=='*') {
            multiply = all_num[all_num.length-2] * all_num[all_num.length-1]
            console.log(multiply)
            document.getElementById("calc-display").value = multiply
            newdisplay = parseInt(document.getElementById("calc-display").value)
            console.log(newdisplay)
            all_num.push(newdisplay)
            console.log(all_num)
        }
        else if (op[op.length-2]=='/') {
            if (all_num[all_num.length-1] == 0 ) {
                alert("Error: divide value could not be zero, please try again!")
                num = []
                op = []
                all_num = []
                dis(val)
            }
            else {
                divide = Math.round(all_num[all_num.length-2] / all_num[all_num.length-1])
                console.log(divide)
                document.getElementById("calc-display").value = divide
                newdisplay = parseInt(document.getElementById("calc-display").value)
                console.log(newdisplay)
                all_num.push(newdisplay)
                console.log(all_num)
            }
        }
    }
}



