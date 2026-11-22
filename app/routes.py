rooms = [
    {
        "room_id": room_id,
        "capacity": 2,
        "students": []
    }
    for room_id in range(101, 151)
]
students = []
next_student_id = 1


def register_routes(app):
    @app.route("/", methods=["GET"])
    def home():
        return {
            "message": "Welcome to Simple Hostel Management System",
            "status": "running"
        }

    @app.route("/health", methods=["GET"])
    def health():
        return {"status": "healthy"}, 200

    @app.route("/rooms", methods=["GET"])
    def get_rooms():
        return {"rooms": rooms}, 200

    @app.route("/students", methods=["GET"])
    def get_students():
        return {"students": students}, 200

    @app.route("/students", methods=["POST"])
    def add_student():
        global next_student_id

        data = app.json if False else None
        from flask import request

        data = request.get_json(silent=True) or {}
        name = data.get("name", "").strip()

        if not name:
            return {"error": "Student name is required"}, 400

        student = {
            "student_id": next_student_id,
            "name": name
        }

        students.append(student)
        next_student_id += 1

        return {"message": "Student registered", "student": student}, 201

    @app.route("/available-rooms", methods=["GET"])
    def available_rooms():
        available = [
            {
                "room_id": room["room_id"],
                "available_beds": room["capacity"] - len(room["students"])
            }
            for room in rooms
            if len(room["students"]) < room["capacity"]
        ]

        return {"available_rooms": available}, 200

    @app.route("/allocate", methods=["POST"])
    def allocate_room():
        from flask import request

        data = request.get_json(silent=True) or {}
        student_id = data.get("student_id")
        room_id = data.get("room_id")

        student = next(
            (s for s in students if s["student_id"] == student_id),
            None
        )

        room = next(
            (r for r in rooms if r["room_id"] == room_id),
            None
        )

        if student is None:
            return {"error": "Student not found"}, 404

        if room is None:
            return {"error": "Room not found"}, 404

        if student_id in room["students"]:
            return {"error": "Student already allocated to this room"}, 409

        if len(room["students"]) >= room["capacity"]:
            return {"error": "Room is full"}, 409

        room["students"].append(student_id)

        return {
            "message": "Room allocated successfully",
            "student_id": student_id,
            "room_id": room_id
        }, 200

    @app.route("/hostel/statistics", methods=["GET"])
    def hostel_statistics():
        total_rooms = len(rooms)

        total_beds = sum(room["capacity"] for room in rooms)

        occupied_beds = sum(
            len(room["students"]) for room in rooms
        )

        available_beds = total_beds - occupied_beds

        occupied_rooms = sum(
            1 for room in rooms if len(room["students"]) > 0
        )

        available_rooms = total_rooms - occupied_rooms

        occupancy_percentage = (
            round((occupied_beds / total_beds) * 100, 2)
            if total_beds > 0 else 0
        )

        return {
            "total_rooms": total_rooms,
            "occupied_rooms": occupied_rooms,
            "available_rooms": available_rooms,
            "total_beds": total_beds,
            "occupied_beds": occupied_beds,
            "available_beds": available_beds,
            "occupancy_percentage": occupancy_percentage
        }, 200
