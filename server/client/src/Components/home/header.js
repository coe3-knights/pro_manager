import React from 'react';
import '../ionicons-2.0.1/css/ionicons.css'
import './homecss/header.css'
import {Link} from '@reach/router'

export function Logo(){
    return(
        <div>
            <figure className='logocontainer'>
                <figcaption className='logocaption'>knight</figcaption>
            </figure>
        </div>
    )
}

export class Login extends React.Component{
    render(){
        const list = ['login'];
        return(
            <div className='login'>
                <ul>
                    {list.map((item)=>{
                        return(
                                <li 
                                key ={item}
                                >
                                {item}
                                </li>
                        )
                    })}
                </ul>
            </div>
        )
    }
}


class About extends React.Component{
    state={
        selectedElement: ''
    };

    handleElement=(item)=>{
        this.setState(()=>{
            return{
                selectedElement: item
            }
        })
    }

    render(){
        const list = ['about us about','open projects openprojects'];
        return(
            <div className='about'>
                <ul>
                   
                    {list.map((item, i)=>{
                        return(
                             <li 
                             style={this.state.selectedElement===item? 
                                {backgroundColor: '#eee'}
                                : {color: '#555'}}
                             onClick={this.handleElement.bind(null, item)}
                             key={item}
                             >
                             {item.split(' ')[0] } {item.split(' ')[1]}
                             </li>
                        )
                    })}
                </ul>
            </div>
        )
    }
}


class Search extends React.Component{
    state = { term: " " };

    onChangeValue = e => {
      this.setState({ term: e.target.value });
    };

    render(){
        return(
            <div className='search'>
                <input onChange = {this.onChangeValue} type='text' className='Search' id='search' placeholder='Search for more ...'></input>
                <label htmlFor='search' className='searchlable'>Search for more ...</label>
               
            </div>
        )
    }
}


class Header extends React.Component{
    render(){
        return(
            <div className='header'>
            <Link to = '/'>
                <Logo />
            </Link>

            <Link to = 'about'>
                <About />
            </Link>
            

                <Search />

            <Link to = 'login'>
                <Login />
            </Link>
            </div>
        )
    }
}

export default Header;