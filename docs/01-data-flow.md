Prefight
- AWS Aurora Serviceless v2

API Gateway: POST api/video/upload
To upload videos to S3

API Gateway: POST api/videos
- Lambda: post-video
  - Verify request body 
  - Update DB: create new video record to AWS Aurora
    {
        URL: str,
        survey_status: "pending"
        survey_result: "None"
    }
  - get return vid
  - create a new SQS record
  - Return vid
- Lambda: process-video
  - Update DB: survey_status to "progressing"
  - verify URL is youtube or internal S3
  - Get audio
  - get survey result from OpenAI
  - Update DB: survey_result: {AI analysis result}
  - Update DB: survey_status to "finish"

API Gateway: Get api/videos/{vid}/survey/status

- Lambda: get-video-survey-status
  - Get DB: 
  - return survey status
{
    status: {pending/progressing/finished},
}

API Gateway: Get api/videos/{vid}/survey/
- Lambda: get-video-survey
  - Get DB: 
  - return survey result
    {
        status: {pending/progressing/finished},
    }

