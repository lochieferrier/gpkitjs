
Variable = function (name,val) {
    // console.log(arguments[0]);

    this.name = name
    this.val = val
    // console.log(name,val)
    this.__plus = function (leftOperand) {
        console.log("adding Count");
        return 909;
    };

};
overload = require('operator-overloading')
