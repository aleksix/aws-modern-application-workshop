// initialization
var score;
var money;
var health;
var happy;
var hunger;
// main
getValue(init);

function init(response)
{
	old_date = response.lastLogin;
	date = (newDate() - old_date)/6000;
	hunger = response.food + date;
	happy = response.entertainment + date;
	score = response.level;
	money = response.money;
	call_health();
	timer();
	save_timer();
}
function is_alive(){
	if (happy > 0 && hunger >0)
		return true;
	else{
		health = 0;
		happy = 0;
		return false;
		}
}
function lvl(){
	return Math.floor(score/10);
}
function max_val(){
	return 99 + lvl/10;	
}
function call_health(){
	if (!is_alive)
		return 0;
	if ((happy + hunger)/2 < max_val)
		return (happy + hunger)/2;
	else
		return max_val;
}

// mechanic
function all_down(){
	if(happy>0)
		happy--;
	if(hunger>0)
		hunger--;
	health = call_health;
}
function up_hunger(value){
	hunger += value;
	if (hunger > max_hunger)
		hunger = max_val;
	health = call_health;
}
function up_happy(value){
	happy += value;
	if (happy > max_val)
		happy = max_val;
	health = call_health;	
}
function up_score(){
	if (score%10 == 9)
		lvl_up();
	score++;
}
function lvl_up(){
	money +=10;
}

// button interatcion
function food(name){
	if (name == "food")
		up_hunger(10);
	if (name == "snack")
		up_hunger(5);
	if (name == "water")
		up_hunger(2);
	POST(hunger)
}
function fun(name){
	if (name == "music")
		up_happy(10);
	if (name == "ball")
		up_happy(7);
	if (name == "talk")
		up_happy(4);
	POST(happy)
}

//Timer

function timer(){
	all_down;
	update_score;
	setTimeout(timer, 6*1000);
}

function save_timer(){
	all_down;
	post;
	setTimeout(save_timer, 300*1000);
}

 $.ajax({
        url : mysfitsApi,
        type : 'GET',
        success : function(response) {
          callback(response);
        },
        error : function(response) {
          console.log("could not retrieve mysfits list.");
          if (response.status == "401") {
             refreshAWSCredentials();
           }
        }
      });

function post(){

$.ajax({
          url : mysfitsApi,
          async : false,
          type : 'POST',
          headers : {'Authorization' : idJwt, 'Content-Type' : 'application/json' },
          data: JSON.stringify({'playerId' : playerId, 'money' : money, 'lastLogin':newDate(), 'food': hunger, 'entertainment': happy, 'level': score}),
          error : function(response) {
            console.log("could not send data.");
            if (response.status == "401") {
               refreshAWSCredentials();
             }
          }
        });
        }

function getValue(callback) {
 $.ajax({
        url : mysfitsApi,
        type : 'GET',
        success : function(response) {
          callback(response);
        },
        error : function(response) {
          console.log("could not get data.");
          if (response.status == "401") {
             refreshAWSCredentials();
           }
        }
      });
}
