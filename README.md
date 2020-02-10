This is the source for [my personal blog](https://andrewstahlman.com).

# Deploying

The Github Actions publish job will build the site and push it to
[staging](http://staging.andrewstahlman.com.s3-website-us-east-1.amazonaws.com/).

Push to prod with the `./publish` script, which just does an `aws s3
cp --recursive` from the staging bucket to the prod bucket.
