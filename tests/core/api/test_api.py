from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse

from .factories import QuestionFactory, AnswerFactory, UserFactory

class QuestionListTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = APIClient()
        cls.token = '92d43661bd7b44d188acd695b09fea5c'
        cls.user = UserFactory(uuid=cls.token)

    @classmethod
    def tearDownClass(cls):
        cls.client = None
        cls.token = None
        UserFactory._meta.model.objects.all().delete()
        cls.user = None
        
    def test_no_questions(self):
        response = self.client.get(reverse('question-list', args=['v1']), {'token': self.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_one_question(self):
        question = QuestionFactory()
        response = self.client.get(reverse('question-list', args=['v1']), {'token': self.token})
        self.assertEqual(response.status_code, 200)
        res_json = response.json()
        self.assertEqual(len(res_json), 1)
        self.assertEqual(res_json[0]['id'], question.id)
        self.assertEqual(res_json[0]['title'], question.title)
        self.assertEqual(res_json[0]['ordinal_number'], question.ordinal_number)

    def test_two_questions(self):
        questions = QuestionFactory.create_batch(2)
        questions.sort(key=lambda i: i.ordinal_number)
        response = self.client.get(reverse('question-list', args=['v1']), {'token': self.token})
        self.assertEqual(response.status_code, 200)
        res_json = response.json()
        self.assertEqual(len(res_json), 2)
        self.assertEqual(res_json[0]['id'], questions[0].id)
        self.assertEqual(res_json[0]['title'], questions[0].title)
        self.assertEqual(res_json[0]['ordinal_number'], questions[0].ordinal_number)
        

class AnswerViewSetTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = APIClient()
        cls.token = '92d43661bd7b44d188acd695b09fea5c'
        cls.user = UserFactory(uuid=cls.token)

    @classmethod
    def tearDownClass(cls):
        cls.client = None
        cls.token = None
        UserFactory._meta.model.objects.all().delete()
        cls.user = None
        
    def test_no_answers(self):
        response = self.client.get(reverse('answer-list', args=['v1']), {'token': self.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])
        
    def test_one_answer(self):
        """tests answer list when is one answer"""
        answer = AnswerFactory(user=self.user)
        response = self.client.get(reverse('answer-list', args=['v1']), {'token': self.token})
        self.assertEqual(response.status_code, 200)
        res_json = response.json()
        self.assertEqual(len(res_json), 1)
        self.assertEqual(res_json[0]['id'], answer.id)
        self.assertEqual(res_json[0]['question'], answer.question.id)
        self.assertEqual(res_json[0]['answer'], answer.answer)
        self.assertEqual(res_json[0]['language'], answer.language)

    def test_two_answers(self):
        """tests answer list when is two answers"""
        answers = AnswerFactory.create_batch(2, user=self.user)
        answers.sort(key=lambda i: i.id)
        response = self.client.get(reverse('answer-list', args=['v1']), {'token': self.token})
        self.assertEqual(response.status_code, 200)
        res_json = response.json()
        self.assertEqual(len(res_json), 2)
        self.assertEqual(res_json[0]['id'], answers[0].id)
        self.assertEqual(res_json[0]['question'], answers[0].question.id)
        self.assertEqual(res_json[0]['answer'], answers[0].answer)
        self.assertEqual(res_json[0]['language'], answers[0].language)
        
    def test_create_answer(self):
        questions = QuestionFactory.create_batch(2)
        answer = 'lore ipsum'
        response = self.client.post('{}?token={}'.format(reverse('answer-list', args=['v1']), self.token), {
                                    'question': questions[0].id, 'answer': answer})
        self.assertEqual(response.status_code, 201)
        res_json = response.json()
        self.assertEqual(res_json['answer'], answer)
        
        
    def test_edit_answer(self):
        answers = AnswerFactory.create_batch(2, user=self.user)
        answer = answers[0]
        answer_new_text = 'ipsum lore'
        url = '{}?token={}'.format(
            reverse('answer-detail', args=['v1', answer.id]), self.token)
        response = self.client.patch(url, {
            'answer': answer_new_text})
        self.assertEqual(response.status_code, 200)
        res_json = response.json()
        self.assertEqual(res_json['id'], answer.id)
        self.assertEqual(res_json['question'], answer.question_id)
        self.assertEqual(res_json['answer'], answer_new_text)