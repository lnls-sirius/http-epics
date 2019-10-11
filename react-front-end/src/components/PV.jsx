import React, { Component } from 'react';
import {getValue} from '../lib/consts';

class PV extends Component {
    constructor(props){
        super(props)
        this.state = {
            name:'',
            value:'',
            host:'',
            severity:''
        }
    }

    componentDidMount() {
        setInterval(()=>{
            getValue(this.props.name, (resp) => { this.setState({...resp})})
        }, 1000);
    }

    render() {
        return (
            <div>
               {this.props.desc}&ensp;&ensp;
               {this.props.name}&ensp;&ensp;&ensp;
               {/* {this.state.severity}&ensp; */}
               {/* {this.state.host}&ensp; */}
               {this.state.value}
            </div>
        )
    }
}
export default PV;
