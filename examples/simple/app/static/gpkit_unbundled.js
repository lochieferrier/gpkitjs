//Global ID counter, used to assign a unique ID to each variable
ID = 0

//ID assignment function
assignID = function(){
    id = ID
    ID++;
    return id
}

//Variable object, derived from gpkit. ID property is hidden to the user, and is used for JSON indexing
Variable = function (name,val) {
    this.name = name
    this.val = val
    this.ID = assignID()
    this.__plus = function (leftOperand) {
        console.log("less than or equal");
        return rightOperand
    };
    this.__lessThanEqual = function (leftOperand) {
        console.log("less than or equal");
        var inequality = new PosynomialInequality(leftOperand,'leq',this)
        return inequality
    };
    this.__greaterThanEqual = function (leftOperand) {
        console.log("greater than or equal");
        var inequality = new PosynomialInequality(leftOperand,'geq',this)
        return inequality
    };
    // this.serialize = function () {
    //     return JSON.stringify(this);
    // };
};

PosynomialInequality  = function(left,oper,right){
    this.left = left
    this.oper = oper
    this.right = right
    // this.serialize = function(){
    //     return JSON.stringify(this);
    // }
}

Model = function (cost,constraints){
    console.log('created model')
    this.cost = cost
    this.constraints = constraints
    this.solution = new Solution()
    
    this.solve = function(solve){
        console.log(this.serialize());
        // var j={"name":"binchen","tree":"forest"};
        // console.log('sending')
        // console.log(JSON.stringify(j))
        $.ajax({
            url: '/index',
            data: this.serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                parsedJSONObj = JSON.parse(response)
                this.solution.variables = parsedJSONObj.variables
                console.log('solution vars')
                console.log(this.solution.variables)
                return this.solution
            },
            error: function(error) {
                console.log(error)
                return error;
            }
        });
    }
    this.serialize = function(){
        return JSON.stringify(this);
    }
}

Solution = function(){
    this.variables = {}
}      
setupNums = function(){
    Number.prototype.__lessThanEqual = function (leftOperand) {
        var inequality = new PosynomialInequality(leftOperand,'leq',this)
        return inequality
    };
    Number.prototype.__greaterThanEqual = function (leftOperand) {
        var inequality = new PosynomialInequality(leftOperand,'geq',this)
        return inequality
    };
    Number.prototype.serialize = function () {
        return JSON.stringify(this)
    };
}

overload = require('operator-overloading')


// // SANDBOX
// var overload = require('operator-overloading');


// //An example Constructor Class
// function Count(val) {
//     var _this = this;
//     this.val = val;
//     this.__plus = function (leftOperand) {
//         console.log("adding Count");
//         leftOperand.val += _this.val;
//         return this;
//     };

//     this.__doubleEqual = function (leftOperand) {
//         console.log('double Equal Check');
//         return _this.val == leftOperand.val;
//     };

//     this.__tripleEqual = function (leftOperand) {
//         console.log('triple Equal Check');
//         return _this.val === leftOperand.val;
//     };
//     this.__lessThanEqual = function(leftOperand){
//         console.log('less than equal')
//         console.log(leftOperand)

//     }
// }

// //We can put in Native types too
// String.prototype.__plus = function (leftOperand) {
//     return (leftOperand + " <added> " + this);
// };

// //Number example
// Number.prototype.__plus = function (leftOperand) {
//     console.log('Adding:', leftOperand, '+', this.valueOf());
//     return leftOperand + this;
// };

// //Number example
// Number.prototype.__lessThanEqual = function (leftOperand) {
//     // console.log('Adding:', leftOperand, '+', this.valueOf());
//     console.log('number fired')
// };

// var v1 = new Count(10);
// var v2 = new Count(20);
// var v3 = new Count(30);

// //That's how you do it. Ity has its own context scope
// var run = overload(function (v1, v2, v3) {

//     var res = v1 + v2 + v3;

//     console.log(3 + 44 + 100);

//     console.log('v1', v1);
//     console.log('v2', v2);
//     console.log('v3', v3);
//     console.log('res', res);

//     // console.log(v1 == v2);
//     // console.log(v1 === v2);

//     console.log('hello' + 'yello' + 'fellow' + 'yo!');

//     console.log(33 + (3 + 3) + 55);

//     var t = 33 || 44;
//     t = 33 && 44;
//     t = 33 & 44;
//     t = 33 | 44;
//     t = 33 ^ 44;
//     t = 33 != 44;
//     t = 33 !== 44;
//     t = 33 < 44;
//     t = 33 > 44;
//     t = 33 >= 44;
//     t = 33 <= 44;
//     t = 33 in [44];
//     t = 33 instanceof Number;
//     t = 33 << 44;
//     t = 33 >> 44;
//     t = 33 >>> 44;
//     t = 33 - 44;
//     t = 33 * 44;
//     t = 33 / 44;
//     t = 33 % 44;
//     t = -44;
//     t = +44;
//     t = ~44;
//     t = ++v1;
//     t = --v1;
//     t = !v1;
//     t += v1;
//     t /= !v2;
//     t *= !v2;
//     t -= !v2;
//     t %= !v2;
//     t <<= !v2;
//     t >>= !v2;
//     t >>>= !v2;
//     t &= !v2;
//     t ^= !v2;
//     t |= !v2;
//     console.log('firing leq')
//     t = v1 <= 10
//     console.log(t)
//     t = v1 + v2 * (!v1 || !v2 && 22) + 33 * 55 / ((4 | ~555) * ~~v2 * +new Date());
//     console.log(t);

// }); //Do this to enable operator overloading in this function. We don't recommend global enablement as that would be confusing.

// //This will be normal operation as defined in JS.
// console.log(3 + 44 + 100);

// run(v1, v2, v3);