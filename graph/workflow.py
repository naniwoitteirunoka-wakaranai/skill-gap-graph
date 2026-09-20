from langgraph.graph import StateGraph, END
from typing import TypedDict


class GraphState(TypedDict):
    student: dict
    job: dict
    matchedSkills: list
    skillGaps: list
    matchScore: int


def compare_skills(state: GraphState):
    student_skills = {
        s["skill"].lower(): s
        for s in state["student"]["skills"]
    }

    matched = []
    gaps = []

    for jd_skill in state["job"]["skills"]:
        if jd_skill["skill"].lower() in student_skills:
            matched.append({
                "skill": jd_skill["skill"],
                "importance": jd_skill["importance"],
                "confidence": student_skills[jd_skill["skill"].lower()]["confidence"],
            })
        else:
            gaps.append({
                "skill": jd_skill["skill"],
                "importance": jd_skill["importance"],
                "reason": "Missing from student profile",
            })

    total = len(state["job"]["skills"])

    score = round(len(matched) / total * 100) if total else 0

    return {
        "matchedSkills": matched,
        "skillGaps": gaps,
        "matchScore": score,
    }


builder = StateGraph(GraphState)
builder.add_node("compare_skills", compare_skills)
builder.set_entry_point("compare_skills")
builder.add_edge("compare_skills", END)

graph = builder.compile()


def run_graph(student, job):
    result = graph.invoke(
        {
            "student": student,
            "job": job,
            "matchedSkills": [],
            "skillGaps": [],
            "matchScore": 0,
        }
    )

    return {
        "matchedSkills": result["matchedSkills"],
        "skillGaps": result["skillGaps"],
        "matchScore": result["matchScore"],
        "summary": {
            "matched": len(result["matchedSkills"]),
            "missing": len(result["skillGaps"]),
            "preferredMissing": 0,
        },
    }