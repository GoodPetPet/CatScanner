import React, {useState,useEffect} from 'react'
import axios from 'axios'

const baseURL="http://127.0.0.1:5000"



function Test() {
  const [post,setPost] = useState<{message:string}|null>(null)

  function createPose() {
    axios.post('http://127.0.0.1:5000/handle_login', {
    }).then(res=>{
      setPost(res.data)
    }).catch(err=>{
      console.log(err)
    })
  }
  return (
    <div>
      <h1>{post?.message||"加载中。。。"}</h1>
      <button className='btn' onClick={createPose}>Create Pose</button>
    </div>
  )
}

export default Test