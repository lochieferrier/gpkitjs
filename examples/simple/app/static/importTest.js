var overload = require('operator-overloading');

function add(a, b){
    return a + b;
};

//Now get another function with operator overloading enabled.
var addWithOverloadingEnabled = overload(add);

//Call with native operator results (Natural)
add(2, 2);

//Call with overloaded operators
addWithOverloadingEnabled(2, 2);
//Another way
overload(add)(2, 2);

//Call with native operator results (Natural)
add(2, 2); //Original method will be untouched always.