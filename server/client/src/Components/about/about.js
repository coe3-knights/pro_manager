import React from 'react'
import './aboutcss/about.css'
import Footer from './aboutfooter'

class About extends React.Component{
    render() {
        return (
            <div className='aboutBack'>
            <div class="row">
                <div class="col-1-of-3">
                     <div className='part1'>

                     </div>
                 </div>
                 <div class="col-1-of-3">
                     <div className='part2'>
                     
                     </div>
                 </div>
                 <div class="col-1-of-3">
                 <div className='part3'>
                     
                 </div> 
                 </div>
            </div>
            <Footer />
            </div>
        )
    }
}

export default About;


// <seaction class="grid">
// <div class="row">
//     <div class="col-1-of-2">
//         1 of 2
//     </div>
//     <div class="col-1-of-2">
//         1 of 2
//     </div>
// </div>
// <div class="row">
//     <div class="col-1-of-3">
//         1 of 3
//     </div>
//     <div class="col-1-of-3">
//         1 of 3
//     </div>
//     <div class="col-1-of-3">
//         1 of 3 
//     </div>
// </div>
// <div class="row">
//     <div class="col-1-of-3">
//         1 of 3      
//     </div>
//     <div class="col-2-of-3">
//         2 of 3
//     </div>
// </div>
// <div class="row">
//     <div class="col-1-of-4">
//         1 of 4
//     </div>
//     <div class="col-1-of-4">
//         1 of 4
//     </div>
//     <div class="col-1-of-4">
//         1 of 4
//     </div>
//     <div class="col-1-of-4">
//         1 of 4
//     </div>
// </div>
// <div class="row">
//     <div class="col-1-of-4">
//         1 of 4
//     </div>
//     <div class="col-1-of-4">
//         1 of 4
//     </div>
//     <div class="col-2-of-4">
//         2 of 4
//     </div>
// </div>
// <div class="row">
//     <div class="col-1-of-4">
//         1 of 4
//     </div>
//     <div class="col-3-of-4">
//         3 of 4
//     </div>
// </div>
// </seaction>

