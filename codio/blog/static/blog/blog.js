class PostRow extends React.Component {
  render () {
    const post = this.props.post

    let thumbnail

    if (post.hero_image.thumbnail) {
      thumbnail = <img src={post.hero_image.thumbnail}/>
    } else {
      thumbnail = '-'
    }

    return <tr>
      <td>{post.title}</td>
      <td>
        {thumbnail}
      </td>
      <td>{post.tags.join(', ')}</td>
      <td>{post.slug}</td>
      <td>{post.summary}</td>
      <td><a href={'/post/' + post.slug + '/'}>View</a></td>
    </tr>
  }
}

class PostTable extends React.Component {
  state = {
    dataLoaded: true,
    data: {
      results: [
        {
          id: 15,
          tags: [
            'django', 'react'
          ],
          'hero_image': {
            'thumbnail': '/media/__sized__/hero_images/1113037_800-thumbnail-100x100-70.jpg',
            'full_size': '/media/hero_images/1113037_800.jpg'
          },
          title: 'Test Post',
          slug: 'test-post',
          summary: 'A test post, created for Django/React.'
        }
      ]
    }
  }

  render () {
    let rows
    if (this.state.dataLoaded) {
      if (this.state.data.results.length) {
        rows = this.state.data.results.map(post => <PostRow post={post} key={post.id}/>)
      } else {
        rows = <tr>
          <td colSpan="6">No results found.</td>
        </tr>
      }
    } else {
      rows = <tr>
        <td colSpan="6">Loading&hellip;</td>
      </tr>
    }

    return <table className="table table-striped table-bordered mt-2">
      <thead>
      <tr>
        <th>Title</th>
        <th>Image</th>
        <th>Tags</th>
        <th>Slug</th>
        <th>Summary</th>
        <th>Link</th>
      </tr>
      </thead>
      <tbody>
      {rows}
      </tbody>
    </table>
  }
}

const domContainer = document.getElementById('react_root')
ReactDOM.render(
  React.createElement(PostTable),
  domContainer
)


// class ClickButton extends React.Component {
//   state = {
//     wasClicked: false
//   }

//   handleClick () {
//     this.setState(
//       {wasClicked: true}
//     )
//     // this.state.wasClicked = true // no setState => no call for render() method. Nothing change on the page
//     // console.log(this.state)
//   }

//   render () {
//     let buttonText

//     if (this.state.wasClicked)
//       buttonText = 'Clicked!'
//     else
//       buttonText = 'Click Me'

//     // return React.createElement(   //(element name or child Component, object (=dict) of properties, children (string or array) )
//     //   'button',
//     //   {
//     //     className: 'btn btn-primary mt-2',
//     //     onClick: () => {
//     //       this.handleClick()   // in this.handleClick directly (without arrow func) 'this' would refer to the event not the component
//     //     }
//     //   },
//     //   buttonText
//     // )
//     // JSX version on above return:
//     return <button
//       className="btn btn-primary mt-2"
//       onClick={
//         () => {
//           this.handleClick()
//         }
//       }
//     >
//       {buttonText}
//     </button>
//   }
// }


// const domContainer = document.getElementById('react_root')
// ReactDOM.render(
//   React.createElement(ClickButton),
//   domContainer
// )



// // function resolvedCallback(data) {
// //   console.log('Resolved with data ' +  data)
// // }

// // function rejectedCallback(message) {
// //   console.log('Rejected with message ' + message)
// // }

// // const lazyAdd = function (a, b) {
// //   const doAdd = (resolve, reject) => {
// //     if (typeof a !== "number" || typeof b !== "number") {
// //       reject("a and b must both be numbers")
// //     } else {
// //       const sum = a + b
// //       resolve(sum)
// //     }
// //   }

// //   return new Promise(doAdd)
// // }

// // const p = lazyAdd(3, 4)
// // // p is a Promise instance that has not yet been settled
// // // There will be no console output at this point.

// // // This next line will settle the doAdd function
// // p.then(resolvedCallback, rejectedCallback) // There will be some console output now

// // lazyAdd("nan", "alsonan").then(resolvedCallback, rejectedCallback)  // chained in a single line


// // // class Greeter {
// // //   constructor (name) {
// // //     this.name = name
// // //   }

// // //   getGreeting () {
// // //     if (this.name === undefined) {
// // //       return 'Hello, no name'
// // //     }

// // //     return 'Hello, ' + this.name
// // //   }

// // //   showGreeting (greetingMessage) {
// // //     console.log(greetingMessage)
// // //   }

// // //   greet () {
// // //     this.showGreeting(this.getGreeting())
// // //   }
// // // }

// // // const g = new Greeter('me')
// // // g.greet()



// // // class DelayedGreeter extends Greeter {
// // //   delay = 2000

// // //   constructor (name, delay) {
// // //     super(name)
// // //     if (delay !== undefined) {
// // //       this.delay = delay
// // //     }
// // //   }

// // //   greet () {
// // //     setTimeout(
// // //       () => {
// // //         this.showGreeting(this.getGreeting())   // inside an arrow function 'this' means not the function itself, but the outer class (!)
// // //       }, this.delay
// // //     )
// // //   }
// // // }
// // // // setTimeout(
// // // //   function() {     // in classic 'function' function, 'this' means the function itself, and inside class we cannot have class methods/atrs through 'this'
// // // //     this.showGreeting(this.getGreeting())  
// // // //   }, this.delay
// // // // )


// // // const dg2 = new DelayedGreeter('Delay 2 Seconds')
// // // dg2.greet()

// // // const dg1 = new DelayedGreeter('Delay 1 Second', 1000)
// // // dg1.greet()



// // // // // alert('Hello, world!')

// // // // for(let i = 0; i < 5; i += 1) {
// // // //   console.log('for loop i: ' + i)
// // // // }

// // // // let j = 0
// // // // while(j < 5) {
// // // //   console.log('while loop j: ' + j)
// // // //   j += 1
// // // // }

// // // // // let j = 10 // error: Previously declared at line ... Without 'let': j=10 ok
// // // // let k = 10

// // // // do {
// // // //   console.log('do while k: ' + k)
// // // // } while(k < 10)

// // // // const numbers = [0, 1, 2, 3, 4] //, 5, 6, 7, 8, 9]

// // // // numbers.forEach((value => {
// // // //   console.log('For each value ' + value)
// // // // }))

// // // // will_be_array_of_undefined = numbers.map(value => console.log(value * 3)) //console numbers ok, but forEach exists
// // // // // console.log(will_be_array_of_undefinde)
// // // // numbers.forEach(value => console.log(value * 3)) 

// // // // const doubled = numbers.map(value => value * 2)  // map
// // // // console.log('Here are the doubled numbers')

// // // // console.log(doubled)


// // // // // function sayHello(yourName) {
// // // // //   if (yourName === undefined) {
// // // // //       console.log('Hello, no name')
// // // // //   } else {
// // // // //        console.log('Hello, ' + yourName)
// // // // //   }
// // // // // }

// // // // // const yourName = 'World'
// // // // // console.log('Before setTimeout')
// // // // // setTimeout(() => {
// // // // //     sayHello(yourName)
// // // // //   }, 2000
// // // // // )
// // // // // console.log('After setTimeout')


// // // // // console.time('myTimer')
// // // // // console.count('counter1')
// // // // // console.log('A normal log message')
// // // // // console.warn('Warning: something bad might happen')
// // // // // console.error('Something bad did happen!')
// // // // // console.count('counter1')
// // // // // console.log('All the things above took this long to happen:')
// // // // // console.timeEnd('myTimer')


// // // // // const theNumber = 1
// // // // // let yourName = 'Ben'

// // // // // if (theNumber === 1) {
// // // // //   let yourName = 'Leo'
// // // // //   // yourName = 'Leo'
// // // // //   alert(yourName)
// // // // // }

// // // // // alert(yourName)



// // // // // 3 ways to declare a function:
// // // // // const myFunction = function() {
// // // // //   //do something
// // // // // }

// // // // // function myFunction() {
// // // // //   //do something
// // // // // }

// // // // // const myFunction = () => {     // good for callbacks with arguments: setTimeout(()=>f(a), 1000)
// // // // //   //do something
// // // // // }
