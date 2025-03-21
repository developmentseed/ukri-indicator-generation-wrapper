cwlVersion: v1.2
$graph:
  - class: Workflow
    id: fetch-hazard-indicator
    label: Fetch a hazard indicator from S3
    doc: Fetch a hazard indicator produced with os_climate_hazard
    requirements:
      ResourceRequirement:
        coresMax: 2
        ramMax: 4096

    inputs:
      hazard_indicator_key:
        type: string
        default: ""
      aws_access_key_id:
        type: string
        default: ""
      aws_secret_access_key:
        type: string
        default: ""
      aws_session_token:
        type: string
        default: ""

    outputs:
      - id: fetched-indicator
        type: Directory
        outputSource:
          - fetch-indicator-step/indicator-results

    steps:
      fetch-indicator-step:
        run: "#fetch-indicator-command"
        in:
          hazard_indicator_key: hazard_indicator_key
          aws_access_key_id: aws_access_key_id
          aws_secret_access_key: aws_secret_access_key
          aws_session_token: aws_session_token
        out:
          - indicator-results


  - class: CommandLineTool
    id: fetch-indicator-command

    hints:
      DockerRequirement:
        dockerPull: indicator-fetching:latest

    requirements:
      ResourceRequirement:
        coresMax: 2
        ramMax: 4096
      NetworkAccess:
        networkAccess: true
      EnvVarRequirement:
          envDef:
            AWS_ACCESS_KEY_ID: $(inputs.aws_access_key_id)
            AWS_SECRET_ACCESS_KEY: $(inputs.aws_secret_access_key)
            AWS_SESSION_TOKEN: $(inputs.aws_session_token)
            AWS_DEFAULT_REGION: "eu-west-2"

    inputs:
      hazard_indicator_key:
        type: string
      aws_access_key_id:
        type: string
      aws_secret_access_key:
        type: string
      aws_session_token:
        type: string

    outputs:
      indicator-results:
        type: Directory
        outputBinding:
          glob: output

    baseCommand: ["prepare-output.sh"]

    arguments:
      - valueFrom: $(inputs.hazard_indicator_key)
