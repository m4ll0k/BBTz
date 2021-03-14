# by m4ll0k 
# github.com/m4ll0k
# jsalert.py - find interesting keywords in javascript files and extract the context..

import sys
import re

R = "\033[1;31m"
B = "\033[1;34m"
G = "\033[1;32m"
W = "\033[1;38m"
Y = "\033[1;33m"
E = "\033[0m"

regexs  = r"(-api|eyJ\S{3,10}|-api-key|-auth|-authorization|-back|-client|-config|-custom|-id|-integration|-oauth|-passwd|-private|-prod|-pwd|-redirect|-scope|-secret|-secure|-swagger|-token|-user|\.bash_history|\.bash_profile|\.cfg|\.client|\.cshrc|\.dockercfg|\.env|\.esmtprc|\.ftpconfig|\.git-credentials|\.history|\.htpasswd|\.ini|\.json|\.pem|\.pgpass|\.pwd|\.remote-sync\.json|\.s3cfg|\.secret|\.secure|\.sh_history|\.sql|\.stg|\.token|\.tugboat|_api|_api-key|_auth|_authorization|_authtoken|_back|_client|_config|_custom|_id|_integration|_oauth|_passwd|_password|_private|_prod|_pwd|_redirect|_scope|_secret|_secure|_token|_user|access_key|access_token|accesskey|accounts\.google\.com|admin_pass|admin_user|algolia_admin_key|algolia_api_key|alias_pass|alicloud_access_key|amazon_secret_access_key|amazonaws|amplitude\.com|ansible_vault_password|aos_key|api|api-|api\.applicationinsights\.io|api\.browserstack\.com|api\.datadoghq\.com|api\.github\.com|api\.googlemaps|api\.ipstack\.com|api\.iterable\.com|api\.keen\.io|api\.mailchimp\.com|api\.mailgun\.net|api\.mapbox\.com|api\.newrelic\.com|api\.pagerduty\.com|api\.sandbox\.paypal\.com|api\.sendgrid\.com|api\.twilio\.com|api\.twitter\.com|api\.wpengine\.com|api_|api_key_secret|api_key_sid|api_secret|apidocs|apikey|apisecret|app_debug|app_id|app_key|app_log_level|app_secret|appkey|appkeysecret|application_key|appsecret|appspot|auth-|auth2|auth_|authorization|authorization-|authorization_|authorizationtoken|authsecret|avastlic|aws_access|aws_access_key_id|aws_bucket|aws_key|aws_secret|aws_secret_key|aws_token|awssecretkey|b2_app_key|back-|back_|bash_history|bash_profile|bashrc|beanstalkd\.yml|bintray_apikey|bintray_gpg_password|bintray_key|bintraykey|bluemix_api_key|bluemix_pass|browserstack_access_key|bucket_password|bucketeer_aws_access_key_id|bucketeer_aws_secret_access_key|built_branch_deploy_key|bx_password|cache_driver|cache_s3_secret_key|cattle_access_key|cattle_secret_key|cccam\.cfg|certificate_password|ci_deploy_password|client-|client-token|client\.|client_|client_token|client_zpk_secret_key|clienttoken|clojars_password|cloud_api_key|cloud_watch_aws_access_key|cloudant_password|cloudflare_api_key|cloudflare_auth_key|cloudinary_api_secret|cloudinary_name|codecov_token|composer\.json|config|config-|config\.|config_|conn\.login|connectionstring|console\.jumpcloud\.com|credentials|cshrc|custom-|custom_|custom_token|cypress_record_key|database|database_password|database_schema_test|datadog_api_key|datadog_app_key|db_password|db_server|db_username|dbeaver-data-sources\.xml|dbpassword|dbuser|deploy\.rake|deploy_password|deployment-config\.json|dhcpd\.conf|digitalocean_ssh_key_body|digitalocean_ssh_key_ids|docker_hub_password|docker_key|docker_pass|docker_passwd|docker_password|dockercfg|dockerhub_password|dockerhubpassword|domain\.freshdesk\.com|dot-files|dotfiles|droplet_travis_password|dynamoaccesskeyid|dynamosecretaccesskey|elastica_host|elastica_port|elasticsearch_password|encryption_password|env\.heroku_api_key|env\.sonatype_password|environment|eureka\.awssecretkey|express\.conf|\.openshift|fabricapisecret|facebook_secret|fb_secret|fcm\.googleapis\.com|filezilla\.xml|firebase|flickr_api_key|fossa_api_key|ftp|ftp_password|gatsby_wordpress_base_url|gatsby_wordpress_client_id|gatsby_wordpress_user|gh_api_key|gh_token|ghost_api_key|git-credentials|gitconfig|github_api_key|github_deploy_hb_doc_pass|github_id|github_key|github_password|github_token|gitlab|gitlab\.example\.com|global|gmail_password|gmail_username|google_maps_api_key|google_private_key|google_secret|google_server_key|googleusercontent|gpg_key_name|gpg_keyname|gpg_passphrase|grant_type|graph\.facebook\.com|graph\.instagram\.com|hapikey|heroku_api_key|heroku_oauth|heroku_oauth_secret|heroku_oauth_token|heroku_secret|heroku_secret_token|herokuapp|history|homebrew_github_api_token|hooks\.slack\.com|htaccess_pass|htaccess_user|htpasswd|id-|id_|id_rsa|id_token|idea14\.key|identitytoolkit\.googleapis\.com|idtoken|incident_channel_name|integration-|integration-key|-internal|_internal|internal-|internal_|integration_|internal|jekyll_github_token|jupyter_notebook_config\.json|jwt_client_secret_key|jwt_lookup_secert_key|jwt_password|jwt_secret|jwt_secret_key|jwt_token|jwt_user|jwt_web_secert_key|jwt_xmpp_secert_key|keypassword|known_hosts|security-token|security_|_security|language:yaml|ldap_password|ldap_username|linux_signing_key|ll_shared_key|location_protocol|log_channel|login|login\.microsoftonline\.com|logins\.json|lottie_happo_api_key|lottie_happo_secret_key|lottie_s3_api_key|lottie_s3_secret_key|mail_password|mail_port|mailchimp|mailchimp_api_key|mailchimp_key|mailgun|mailgun_key|mailgun_password|mailgun_priv_key|mailgun_secret_api_key|makefile|manage_key|mandrill_api_key|mapbox|mapbox_apikey|master\.key|master_key|mg_api_key|mg_public_api_key|mh_apikey|mh_password|mile_zero_key|minio_access_key|minio_secret_key|mix_pusher_app_cluster|mix_pusher_app_key|mydotfiles|mysql|mysql_root_password|netlify_api_key|netrc|nexus_password|node_env|node_pre_gyp_accesskeyid|node_pre_gyp_secretaccesskey|npm_api_key|npm_password|npm_secret_key|npmrc|nuget_api_key|nuget_apikey|nuget_key|oauth-|oauth2|oauth2\.googleapis\.com|oauth_|object_storage_password|octest_app_password|octest_password|okta_key|omise_key|onesignal_api_key|onesignal_user_auth_key|openwhisk_key|org_gradle_project_sonatype_nexus_password|org_project_gradle_sonatype_nexus_password|os_password|ossrh_jira_password|ossrh_pass|ossrh_password|pagerduty_apikey|parse_js_key|passwd-|passwd_|password_|passwords|paypal_secret|paypal_token|personal_key|pgpass|playbooks_url|plotly_apikey|plugin_password|postgres_env_postgres_password|postgresql_pass|preprod|private|private-|private_|private_signing_password|prod|prod-|prod\.access\.key\.id|prod\.exs|prod\.secret\.exs|prod\.secret\.key|prod_|prod_password|proftpdpasswd|pt_token|publish_key|pusher_app_id|pwd-|pwd_|queue_driver|rabbitmq_password|rds\.amazonaws\.com|recentservers\.xml|redirect-|redirect_|redirect_uri|redis_password|registry\.npmjs\.org|response_auth_jwt_secret|rest_api_key|returnsecuretoken|rinkeby_private_key|robomongo\.json|root_password|ropsten_private_key|route53_access_key_id|rtd_key_pass|rtd_store_pass|s3_access_key|s3_access_key_id|s3_key|s3_key_app_logs|s3_key_assets|s3_secret_key|s3cfg|salesforce_password|sandbox_aws_access_key_id|sandbox_aws_secret_access_key|sauce_access_key|saucelabs\.com|scope=|scope_|secret-|secret\.password|secret_|secret_access_key|secret_bearer|secret_key_base|secretaccesskey|secrets|secrets\.yml|secure-|secure_|securetoken|security_credentials|send\.keys|send_keys|sendgrid_api_key|sendgrid_key|sendgrid_password|sendgrid_token|sendkeys|server\.cfg|ses_access_key|ses_secret_key|setdstaccesskey|setsecretkey|settings|settings\.py|sf_username|sftp-config\.json|sftp\.json|\.vscode|shodan_api_key|sid_token|signing_key_password|signing_key_secret|slack\.com|slack_api|slack_channel|slack_key|slack_outgoing_token|slack_signing_secret|slack_webhook|slash_developer_space_key|snoowrap_password|socrata_password|sonar_organization_key|sonar_project_key|sonatype_password|sonatype_token_password|soundcloud_password|spec|sql_password|sqsaccesskey|square_access_token|square_token|squaresecret|squareup\.com|ssh|ssh2_auth_password|sshd_config|sshpass|staging|stg|storepassword|stormpath_api_key_id|stormpath_api_key_secret|strip_key|strip_secret_key|stripe|stripe_key|stripe_secret|striptoken|svn_pass|swagger|swagger-|tenant_id|tesco_api_key|tester_keys_password|testuser|thera_oss_access_key|token-|token\.|token=|token_|trusted_hosts|tugboat|twilio_account_id|twilio_account_secret|twilio_account_sid|twilio_accountsid|twilio_acount_sid|twilio_api|twilio_api_auth|twilio_api_key|twilio_api_secret|twilio_api_sid|twilio_api_token|twilio_secret|twilio_secret_token|twilio_sid|twilio_token|twilioapiauth|twiliosecret|twine_password|twitter_secret|twitterkey|userid|userid-|userid_|ventrilo_srv\.ini|verifycustomtoken|wakatime\.com|webhook|webservers\.xml|wp-config|wp-config\.php|www\.googleapis\.com|x-api-key|zen_key|zen_tkn|zen_token|zendesk_api_token|zendesk_key|zendesk_token|zendesk_url|zendesk_username|s3\.amazonaws\.com|s3\.console\.aws\.amazon\.com|eyJ\w+|\.onmessage|\.postmessage|_session|session_|-session|HOMEBREW_GITHUB_API_TOKEN|ssh_key|sshkey|token|username|xoxa-2|xoxr|private-key|ssh:\/\/|ftp:\/\/|ws:\/\/|wss:\/\/|client_secret|clientsecret|consumer_key|consumer_secret|dbpasswd|encryption-key|encryption_key|encryptionkey|_encryption|-encryption|encryption_|encryption-|dencryption_|_dencryption|id_dsa|irc_pass|key_|_key|key-|-key|oauth_token|pass|password|private_key|privatekey|secret|secret-key|secret_key|secret_token|secretkey|session_key|session_secret|slack_api_token|slack_secret_token|slack_token|ssh-key|aws_secret_access_key|bearer|bot_access_token|bucket|client-secret|client_id|client_key|accesstoken|api-key|api_key|api_secret_key|api_token|auth_token|authkey|ConsumerSecret|consumer_|_consumer|consumer-|-consumer|merchant|-merchant|merchant-|_merchant|merchant_|sq0csp-|_live|live_|-live|live-|-sandbox|_sandbox|sandbox_|sandbox-|_stg|-stg|stg-|stg_|gtoken|gidtoken|acctoken|acc_token|access_|_access|-access|access-|dev_|_dev|developer_|_developer|-developer|developer-|authtoken|myaccesstoken)"


try:
    import jsbeautifier
    import requests
    import urllib3
except Exception as e:
    sys.exit(print("{0}.. please download this module/s".format(e)))

urllib3.disable_warnings(
	urllib3.exceptions.InsecureRequestWarning
)

def beauty(content:str)->str:
    return jsbeautifier.beautify(content.decode())

def getjs(url:str)->dict:
    try: return requests.get(url,verify=False) 
    except: return {'content':None}

def main()->None:
    try:
        url = sys.argv[1]
    except:
        sys.exit(print("\nUsage:\tpython3 {0} <url> <regex|string>\n".format(sys.argv[0])))
    if '.js' in url:
        r = getjs(url)
        if r.status_code == 200:
            js = beauty(r.content)
            for j in js.split('\n'):
                rr = re.findall(regexs,j,re.I)
                if rr:
                    rr = list(set(rr))
                    k = js.index(j)
                    a = js[js.index(j)-100 : js.index(j)+100]
                    for i in rr:
                        a = a.replace(i,f'{R}{i}{E}{Y}')
                    print(f'l:{G}{W}{str(k)}{E} -> {",".join(rr)}{E}\n{"-"*100}\n{Y}{a}{E}\n')
    else:
        sys.exit(print("\".js\" not found in URL ({}).. check your url".format(sys.argv[1])))

main()
