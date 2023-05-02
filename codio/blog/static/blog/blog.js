// alert('Hello, world!')

for(let i = 0; i < 5; i += 1) {
  console.log('for loop i: ' + i)
}

let j = 0
while(j < 5) {
  console.log('while loop j: ' + j)
  j += 1
}

// let j = 10 // error: Previously declared at line ... Without 'let': j=10 ok
let k = 10

do {
  console.log('do while k: ' + k)
} while(k < 10)

const numbers = [0, 1, 2, 3, 4] //, 5, 6, 7, 8, 9]

numbers.forEach((value => {
  console.log('For each value ' + value)
}))

will_be_array_of_undefined = numbers.map(value => console.log(value * 3)) //console numbers ok, but forEach exists
// console.log(will_be_array_of_undefinde)
numbers.forEach(value => console.log(value * 3)) 

const doubled = numbers.map(value => value * 2)  // map
console.log('Here are the doubled numbers')

console.log(doubled)


// function sayHello(yourName) {
//   if (yourName === undefined) {
//       console.log('Hello, no name')
//   } else {
//        console.log('Hello, ' + yourName)
//   }
// }

// const yourName = 'World'
// console.log('Before setTimeout')
// setTimeout(() => {
//     sayHello(yourName)
//   }, 2000
// )
// console.log('After setTimeout')


// console.time('myTimer')
// console.count('counter1')
// console.log('A normal log message')
// console.warn('Warning: something bad might happen')
// console.error('Something bad did happen!')
// console.count('counter1')
// console.log('All the things above took this long to happen:')
// console.timeEnd('myTimer')


// const theNumber = 1
// let yourName = 'Ben'

// if (theNumber === 1) {
//   let yourName = 'Leo'
//   // yourName = 'Leo'
//   alert(yourName)
// }

// alert(yourName)



// 3 ways to declare a function:
// const myFunction = function() {
//   //do something
// }

// function myFunction() {
//   //do something
// }

// const myFunction = () => {     // good for callbacks with arguments: setTimeout(()=>f(a), 1000)
//   //do something
// }