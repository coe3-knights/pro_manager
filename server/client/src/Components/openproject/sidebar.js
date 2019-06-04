import React from 'react';
import  {NavLink} from 'react-router-dom'
//import styled from 'styled-components';

class SideBar extends React.Component{
    state={
        selectedElement: 'ion-ios-folder-outline folder folders' 
    };

    handleElement=(item)=>{
        this.setState(()=>{
            return{
                selectedElement: item
            }
        })
    }
    render() {
    const list = ['ion-ios-drag manu manu',
     'ion-ios-bell-outline notification notification',
     'ion-ios-folder-outline folder folders',
     'ion-ios-chatboxes-outline chart chart',
     'ion-ios-cart-outline store store',
     'ion-ios-contact-outline profile profile',
     'ion-ios-cog-outline settings settings'];

      return (
        <div>
          <ul className='sidelinks'>
            {list.map((item, i)=>{
                let names = list[i].split(' ')[1]
                let name = list[i].split(' ')[2]
                return(
                  <NavLink to={`/${name}`}>
                    <li
                     style={this.state.selectedElement===item? 
                        {backgroundColor: 'green'}
                        : {color: '#aaa'}}
                     onClick={this.handleElement.bind(null, item)}
                     key={item} 
                     className={item}
                    >
                     <span className='pops'>{names}</span>
                    </li>
                  </NavLink>
                )
            })}
          </ul>
        </div>
      )
    }
}

export default SideBar;