import React, { useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { Redirect,useHistory } from "react-router-dom";
import { addPost } from "../../store/post";
import ImageUploadComponent from "./ImageUploadComponent";
import './NavBar.css'

const PostForm = ({ onClose }) => {
  const [errors, setErrors] = useState([]);
  const [caption, setCaption] = useState("");
  const [url, setUrl] = useState("");
  const user = useSelector((state) => state.session.user);
  const dispatch = useDispatch();
  const history = useHistory();

  const onPostSubmit = async (e) => {
    // Need to create a function that posts to database
    e.preventDefault();
    if(user){
      let post = {
                  userId: user.id,
                  caption: caption,
                  imgUrl: url
                }
      if(url){
        return await dispatch(addPost(post))
        .then((res)=>{
          // console.log(res);
          if(res){
            setErrors(res)

          }
          else{
            history.push(`/${user.id}`)

            onClose()

          }
        })
    }
      else{
        window.alert('you must upload an image')
      }

    }
  };

  const updateCaption = (e) => {
    setCaption(e.target.value);
  };

  const updateUrl = (e) => {
    setUrl(e.target.value);
  };

  return (
    <div className="post-form-wrapper">
      <ImageUploadComponent setUrl={setUrl} />
      <form className="post-form-container" onSubmit={onPostSubmit}>
        <div>
          {errors.map((error, ind) => (
            <div key={ind}>{error}</div>
          ))}
        </div>
        <div className="post-form-children">
          <input
            className="post-form-input-text-boxes"
            name="caption"
            type="text"
            placeholder="Caption"
            value={caption}
            onChange={updateCaption}
          />
        </div>
        <div className="post-form-children">
          <button className="post-form-default-submit-button" type="submit">
            Post
          </button>
        </div>
      </form>
    </div>
  );
};

export default PostForm;
