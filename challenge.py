from flask import Flask, jsonify, request

app = Flask(__name__)


class Member:
    CHILD = 'CHILD'
    SPOUSE = 'SPOUSE'
    SIBLING = 'SIBLING'

    relations = [CHILD, SPOUSE, SIBLING]

    def __init__(self, name):
        self.name = name
        self.relationships = []

    def relationship_with(self, member, relation):
        if not any((m, r) == (member, relation) for m, r in self.relationships):
            self.relationships.append((member, relation))
            if relation in Member.relations:
                member.relationships.append((self, relation))
        else:
            return False

    def get_closest_relationship(self, target):
        visited = set()
        queue = [(self, 0)]

        while queue:
            current, distance = queue.pop(0)
            visited.add(current)

            if current == target:
                return distance

            for member, _ in current.relationships:
                if member not in visited:
                    queue.append((member, distance + 1))

        return None


class FamilyTreeAPI:
    def __init__(self):
        self.members = {}

    def create_member(self, name):
        if name not in self.members:
            self.members[name] = Member(name)
        else:
            return False
        return self.members[name]

    def define_relationship(self, member1_name, member2_name, relation):
        member1 = self.members.get(member1_name)
        member2 = self.members.get(member2_name)

        if not member1:
            member1 = self.create_member(member1_name)
        if not member2:
            member2 = self.create_member(member2_name)

        member1.relationship_with(member2, relation)

    def get_relationship(self, member1_name, member2_name):
        member1 = self.members.get(member1_name)
        member2 = self.members.get(member2_name)

        if member1 and member2:
            return member1.get_closest_relationship(member2)
        else:
            return None


family_tree = FamilyTreeAPI()

# family_tree.define_relationship('Jimmy Doe', 'Jenny Doe', Member.CHILD)
# family_tree.define_relationship('Jezza Doe', 'Jimmy Doe', Member.CHILD)
# family_tree.define_relationship('John Doe', 'Jenny Doe', Member.CHILD)
# family_tree.define_relationship('Jane Doe', 'John Doe', Member.SPOUSE)
# family_tree.define_relationship('James Doe', 'Jane Doe', Member.SIBLING)
# family_tree.define_relationship('Jason Doe', 'James Doe', Member.CHILD)
# family_tree.define_relationship('Jezza Doe', 'Jason Doe', Member.SPOUSE)

# print(family_tree.get_relationship('James Doe', 'Jenny Doe'))
# print(family_tree.get_relationship('John Doe', 'James Doe'))
# print(family_tree.get_relationship('Jenny Doe', 'Jane Doe'))
# print(family_tree.get_relationship('Jason Doe', 'Jason Doe'))


@app.route('/add-member', methods=['POST'])
def create_member_api():
    """API endpoint to create a new member."""
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    response = family_tree.create_member(name)
    if response is False:
        return jsonify({'message': f'Member {name} already exist'}), 403
    return jsonify({'message': f'Member {name} created'}), 201

@app.route('/add-relationship', methods=['POST'])
def add_relationship():
    """API endpoint to define a relationship."""
    data = request.get_json()
    member1_name = data.get('member1_name')
    member2_name = data.get('member2_name')
    relation = data.get('relation')
    if not all([member1_name, member2_name, relation]):
        return jsonify({'error': 'All fields are required'}), 400
    family_tree.define_relationship(member1_name, member2_name, relation)
    return jsonify({'message': f'Relationship defined between {member1_name} and {member2_name}'}), 201

@app.route('/get-relationship', methods=['POST'])
def get_relationship():
    """API endpoint to get the relationship."""
    data = request.get_json()
    member1_name = data.get('member1_name')
    member2_name = data.get('member2_name')
    if not all([member1_name, member2_name]):
        return jsonify({'error': 'Both member names are required'}), 400

    closest_count = family_tree.get_relationship(member1_name, member2_name)
    if closest_count is not None:
        return jsonify({'closest_count': closest_count}), 200
    else:
        return jsonify({'error': 'No relationship found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
