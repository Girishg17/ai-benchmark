from enum import Enum

class TaskType(str,Enum):
    CODING = "coding"
    GENERAL = "general"
    TRANSLATION = "translation"
    REASONING = "reasoning"
    SUMMARIZATION = "summarization"
    MATH = "math"
    IMAGE_GENERATION = "image_generation"

def classify_task(question:str)->TaskType:
    q= question.lower()
    coding_keywrods = ["code","program","implement","function","class","algorithm","script","debug","compile","syntax","java","python","javascript","c++","ruby","html","css"]
    translation_keywords = ["translate","translation","in english","in spanish","in french","in german","in chinese","in japanese","in russian"]
    reasoning_keywords = ["why","how","explain","reason","cause","effect","analyze","interpret"]
    summarization_keywords = ["summarize","summary","brief","condense","shorten","main points","key points"]        
    math_keywords = ["calculate","solve","equation","math","geometry","algebra","arithmetic","number","sum","difference","product","quotient"]
    image_generation_keywords = ["generate image","create image","draw","illustrate","picture of","visualize","design"]

    if any (keywords in  q for keywords in coding_keywrods):
        return TaskType.CODING
    elif any (keywords in  q for keywords in translation_keywords):
        return TaskType.TRANSLATION
    elif any (keywords in  q for keywords in reasoning_keywords):
        return TaskType.REASONING
    elif any (keywords in  q for keywords in summarization_keywords):
        return TaskType.SUMMARIZATION
    elif any (keywords in  q for keywords in math_keywords):
        return TaskType.MATH
    elif any (keywords in  q for keywords in image_generation_keywords):
        return TaskType.IMAGE_GENERATION
    else:
        return TaskType.GENERAL
           