let a = [2,3,61,123,12];

// for (const i of a){
//     if (i % 6 ==0){
//         console.log(i);
//         return i
//     }else if (a.indexOf(i)+1 === a.length){
//         console.log(-1);
//         return -1
//     }
// }
console.log(multiploDeSeis(a))

function multiploDeSeis(a) {
    return a.find(i => i % 6 === 0) || -1
  }