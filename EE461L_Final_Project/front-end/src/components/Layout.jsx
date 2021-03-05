import React from 'react'
import HeaderMenu from './HeaderMenu'

export default function Layout(props) {
    return (
        <div>
            <HeaderMenu/>
            {props.children}

        </div>
    )
}
