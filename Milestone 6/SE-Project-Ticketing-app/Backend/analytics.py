import matplotlib.pyplot as plt

# Query to get the count of resolved and unresolved tickets
resolved_count = Ticket.query.filter_by(ticket_status='resolved').count()
unresolved_count = Ticket.query.filter_by(ticket_status='unresolved').count()

# Pie chart
labels = ['Resolved', 'Unresolved']
sizes = [resolved_count, unresolved_count]
colors = ['#ff9999', '#66b3ff']

plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.title('Resolved vs Unresolved Threads')
plt.show()




#
#
# Assuming you have a 'timecreation' column in Ticket to track ticket creation time
# Query to get the count of resolved queries within and delayed
twenty_four_hours_ago = datetime.now() - timedelta(hours=24)

resolved_within_count = Ticket.query.filter(
    Ticket.ticket_status == 'resolved',
    Ticket.timecreation >= twenty_four_hours_ago
).count()

delayed_count = resolved_count - resolved_within_count

# Pie chart
labels = ['Resolved Within 24hrs', 'Delayed']
sizes = [resolved_within_count, delayed_count]
colors = ['#99ff99', '#ffcc99']

plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.title('Resolved Queries: Within 24hrs vs Delayed')
plt.show()

#
from sqlalchemy import func

# Query to get support staff wise issue handling
staff_issues = db.session.query(
    Staff.username,
    func.count(Ticket.ticket_id).label('issue_count')
).join(Ticket).group_by(Staff.username).all()

# Convert the result to a dictionary for easier plotting
staff_names = [item[0] for item in staff_issues]
issue_counts = [item[1] for item in staff_issues]

# Bar chart
plt.bar(staff_names, issue_counts, color='#66b3ff')
plt.xlabel('Support Staff')
plt.ylabel('Number of Issues Handled')
plt.title('Support Staff Wise Issue Handling')
plt.xticks(rotation=45)
plt.show()
