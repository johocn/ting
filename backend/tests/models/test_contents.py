import pytest
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.contents import Content, Question, ContentQuizConfig

class TestContentModel:
    """内容模型测试"""
    
    def test_create_content(self, db_session: Session):
        """测试创建内容"""
        content = Content(
            title="测试视频",
            url="https://example.com/test.mp4",
            duration=1800,  # 30分钟
            category="education",
            reward_points_per_minute=5,
            status=True
        )
        db_session.add(content)
        db_session.commit()
        
        assert content.id is not None
        assert content.title == "测试视频"
        assert content.url == "https://example.com/test.mp4"
        assert content.duration == 1800
        assert content.category == "education"
        assert content.reward_points_per_minute == 5
        assert content.status == True
        assert content.created_at is not None
    
    def test_create_question(self, db_session: Session):
        """测试创建问题"""
        content = Content(
            title="测试视频2",
            url="https://example.com/test2.mp4",
            duration=1200,
            category="entertainment",
            reward_points_per_minute=3
        )
        db_session.add(content)
        db_session.commit()
        
        question = Question(
            content_id=content.id,
            question_text="这是什么类型的视频？",
            options={"A": "教育", "B": "娱乐", "C": "科技", "D": "生活"},
            correct_answer="B",
            individual_points=20,
            question_order=1
        )
        db_session.add(question)
        db_session.commit()
        
        assert question.id is not None
        assert question.content_id == content.id
        assert question.question_text == "这是什么类型的视频？"
        assert question.options == {"A": "教育", "B": "娱乐", "C": "科技", "D": "生活"}
        assert question.correct_answer == "B"
        assert question.individual_points == 20
        assert question.question_order == 1
    
    def test_create_quiz_config(self, db_session: Session):
        """测试创建答题配置"""
        content = Content(
            title="测试视频3",
            url="https://example.com/test3.mp4",
            duration=2400,
            category="tech"
        )
        db_session.add(content)
        db_session.commit()
        
        config = ContentQuizConfig(
            content_id=content.id,
            total_questions=10,
            required_correct=8,
            pass_percentage=80,
            quiz_points=100,
            time_limit=3600,  # 1小时
            allow_retry=True,
            retry_limit=3
        )
        db_session.add(config)
        db_session.commit()
        
        assert config.id is not None
        assert config.content_id == content.id
        assert config.total_questions == 10
        assert config.required_correct == 8
        assert config.pass_percentage == 80
        assert config.quiz_points == 100
        assert config.time_limit == 3600
        assert config.allow_retry == True
        assert config.retry_limit == 3
    
    def test_content_with_questions(self, db_session: Session):
        """测试内容与问题关联"""
        content = Content(
            title="测试视频4",
            url="https://example.com/test4.mp4",
            duration=1800,
            category="education"
        )
        db_session.add(content)
        db_session.commit()
        
        # 创建多个问题
        questions = []
        for i in range(3):
            question = Question(
                content_id=content.id,
                question_text=f"问题{i+1}",
                options={"A": "选项A", "B": "选项B"},
                correct_answer="A",
                individual_points=20,
                question_order=i+1
            )
            db_session.add(question)
            questions.append(question)
        
        db_session.commit()
        
        # 验证问题数量
        content_questions = db_session.query(Question).filter(
            Question.content_id == content.id
        ).all()
        
        assert len(content_questions) == 3
        for i, q in enumerate(content_questions):
            assert q.question_order == i + 1
            assert q.individual_points == 20
