import React from 'react';
import {Link} from '@reach/router'
import './homecss/img.css'
import './homecss/grid.css'

export const Social=()=>{
    let list = ['ion-social-whatsapp-outline what','ion-social-twitter-outline twit','ion-social-skype-outline skyp','ion-social-googleplus-outline goog']
  
    return(
        <ul className='social'>
            {list.map((item)=>{
                return(
                        <li key={item}
                        className={item}
                        >
                            &nbsp;
                        </li>
                )
            })}
        </ul>
    )
}

const Img=()=>{
    return(
        <div className="row">
            <div className="col-1-of-2 hero">
                <Social />
            </div>
            <div className="col-1-of-2 right">
                <div className='rightside'>
                <h1 className="main_header">
                    <span className="primary_txt1">knight </span>
                    <span className="primary_txt2">project management</span>
                </h1>
                <p><span>We offer the best project management</span><span> for students accros the world</span></p>
                <div className='getstartedbox'>
                <Link to = 'signup'>
                    <p className='getstarted' >s i g n u p</p>
                </Link> 
                </div>
                </div>
            </div>
        </div>
    )
}


export default Img;