var rate1 = document.getElementById("rate-1");
var rate2 = document.getElementById("rate-2");
var rate3 = document.getElementById("rate-3");
var rate4 = document.getElementById("rate-4");
var rate5 = document.getElementById("rate-5");
var rate6 = document.getElementById("rate-6");
var rate7 = document.getElementById("rate-7");
var rate8 = document.getElementById("rate-8");
var rate9 = document.getElementById("rate-9");
var rate10 = document.getElementById("rate-10");

var valueTemp = 0;
console.log(valueTemp);
function addNum(num){
    document.getElementById("score").innerHTML = num;
}
function removeNum(){
    document.getElementById("score").innerHTML = valueTemp;
}
function score(){

    if (rate1.checked){
        document.getElementById("score").innerHTML = "1";
        valueTemp = 1;
    }
    else if (rate2.checked){
        document.getElementById("score").innerHTML = "2";
        valueTemp = 2;
    }
    else if (rate3.checked){
        document.getElementById("score").innerHTML = "3";
        valueTemp = 3;
    }
    else if (rate4.checked){
        document.getElementById("score").innerHTML = "4";
        valueTemp = 4;
    }
    else if (rate5.checked){
        document.getElementById("score").innerHTML = "5";
        valueTemp = 5;
    }
    else if (rate6.checked){
        document.getElementById("score").innerHTML = "6";
        valueTemp = 6;
    }
    else if (rate7.checked){
        document.getElementById("score").innerHTML = "7";
        valueTemp = 7;
    }
    else if (rate8.checked){
        document.getElementById("score").innerHTML = "8";
        valueTemp = 8;
    }
    else if (rate9.checked){
        document.getElementById("score").innerHTML = "9";
        valueTemp = 9;
    }
    else if (rate10.checked){
        document.getElementById("score").innerHTML = "10";
        valueTemp = 10;
    }

}