# TeamworkPM
Teamwork PM Status Integration

Project to grab Teamwork PM Status information on Friday to see who posted between Monday and Thursday.

The idea is that this info can be harvested to track metrics against a company expectation that folks will use the Status functionality within Teamwork PM to post the top three items they are working on that week. That status information is harvested by a different script on Friday mornings and shared as a text file with all company personnel as a means of improving communications and workload visibility.

The weekly files generated by this script can be parsed to obtain compliance metrics across a given period of time.

Teamwork PM requires the generation of an API key via their site prior to integration access.

The harvesting script requires two environment variables associated with Teamwork PM integration:

TEAMWORKPM_API_KEY

TEAMWORKPM_SUBDOMAIN

Add these to your .bashrc


export TEAMWORKPM_API_KEY=myapikey

export TEAMWORKPM_SUBDOMAIN=usually-company-name

Don't forget to source your .bashrc after changes. E.g.,

. ~/.bashrc
