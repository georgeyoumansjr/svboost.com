# Branching Strategy

About the branch strategy, we can make use of Two of then:

 - You can create a branch to add a batch of features or updates from
 the same kind or an epic label on SEAnalytics Jira Kanban. Once everything's done,
 the given branch will be merged with master, after passing review of course, by creating a 
 pull request.
 
 - You can create a branch for every specific new feature or update. This is because
 one feature can have many updates or new stuff to add. One branch for a batch of features can
 get complicated if there is a lot of work to do, and like this the commits from different feature
 might get mixed and this might produce unwanted changes when we want to revert the branch to a specific
 point, mainly when we want to revert some changes done. So each feature should reference one card in Jira 
 that describes the feature or task at hand by using the id of the card in the name of the 
 branch like: `sena-12/name-of-the-branch`.