<p> In settings.py SECRET_KEY is not defined</p>
<p>SIMPLE_JWT = {<br>
    "ACCESS_TOKEN_LIFETIME": timedelta(days=),<br>
    "REFRESH_TOKEN_LIFETIME":timedelta(days=)<br>
    You also have to define days to use JWT auth. Its a expiry (of jwt token) in days you can make it seconds or minutes also.
</p>
<br>
<hr>
<br>
<h4>It is not trained with many images only 7000 (3500- gun image , 3500- other image)</h4>
<p>if more then 0.5 then it could be a gun else not a gun<p>
<h4>trained in low image size which is 120x120 {resize it yourself one by one or use cv2.resize)</h4>
<p>100 times epoch mean 100 times studied all images</p>
<p>at the time 98% accuracy - 80% test accuracy which is very low</p>
<br>
<hr>
<br>
<p>
URLS:<br>
-POST /api/reg/staff - registration of the staff members<br>
<br>
-POST /api/reg- user registration<br>
<br>
- POST /api/authenticate - JWT token.<br>
- INPUT: Email, Password<br>
- RETURN: JWT token<br>
<br>
- POST /api/follow/{id} authenticated user follow user with {id}<br>
<br>
- POST /api/unfollow/{id} authenticated user unfollow a user with {id}<br>
<br>
- GET /api/user should authenticated user not necessary account holder return the respective user profile. Like you can see other likes and followers if you are login in insta.<br>
- RETURN: User Name, number of followers & followings.<br>
<br>
- POST api/posts/ would add a new post created by the authenticated user.<br>
- Input: Title, Description<br>
- RETURN: Post-ID, Title, Description, Created Time(UTC).<br>
<br>
- DELETE api/posts/{id} would delete post with {id} created by the authenticated user.<br>
<br>
- POST /api/like/{id} would like the post with {id} by the authenticated user.<br>
<br>
- POST /api/unlike/{id} would unlike the post with {id} by the authenticated user.<br>
<br>
- POST /api/comment/{id} add comment for post with {id} by the authenticated user.<br>
- Input: Comment<br>
- Return: Comment-ID<br>
 <br>
- GET api/posts/{id} would return a single post with {id} populated with its number of likes and comments<br>
<br>
- GET /api/all_posts would return all posts created by authenticated user sorted by post time.<br>
- RETURN: For each post return the following values<br>
- id: ID of the post<br>
- title: Title of the post<br>
- desc: Description of the post<br>
- created_at: Date and time when the post was created<br>
- all comments: Array of comments, for the particular post<br>
- likes: Number of likes for the particular post<br>
<br>
- GET /api/all would return all posts created by authenticated user sorted by post time.<br>
- RETURN: For each post return the following values<br>
- full name<br>
- id: ID of the post<br>
- title: Title of the post<br>
- desc: Description of the post<br>
- created_at: Date and time when the post was created<br>
- all comments: Array of comments, for the particular post<br>
- likes: Number of likes for the particular post<br>
- following<br>
- followers<br>
<br>
 </p>
