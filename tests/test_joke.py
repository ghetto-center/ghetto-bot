# -*- coding: utf-8 -*-
import unittest
from joke import mamka, anus, anus_rude, how_you_doing, is_good, is_plan, fag_reply


class TestJokeClass(unittest.TestCase):

    def test_mamka(self):
        self.assertEqual(
            mamka('Никит, что вчера делал?'),
            'Вчера мамку твою делал')
        self.assertEqual(mamka('фыдваодфывоа'), None)

    def test_anus(self):
        self.assertEqual(anus('Никит, что вчера делал?'), 'Анус себе делай')
        self.assertEqual(anus('фыдваодфывоа'), None)

    def test_anus_rude(self):
        self.assertEqual(
            anus_rude('Никит, что вчера делал?'),
            'Анус себе делай, пес')
        self.assertEqual(anus_rude('фыдваодфывоа'), None)

    def test_how_you_doing(self):
        self.assertEqual(
            how_you_doing(
                'Никит, что вчера делал?',
                ['test']),
            None)
        self.assertNotEqual(
            how_you_doing(
                'как сам?',
                ['Как сала килограмм!']),
            None)
        self.assertNotEqual(
            how_you_doing(
                'как сам-то?',
                ['Как сала килограмм!']),
            None)
        self.assertEqual(
            how_you_doing(
                'как сам?',
                ['Как сала килограмм!']),
            'Как сала килограмм!')
        self.assertEqual(
            how_you_doing(
                'как сам?',
                ['Как пустой универсам!']),
            'Как пустой универсам!')
        self.assertEqual(
            how_you_doing(
                'asdf каК   сАм ? xxx ',
                ['Как пустой универсам!']),
            'Как пустой универсам!')
        self.assertEqual(
            how_you_doing(
                'как сам  ',
                ['Как пустой универсам!']),
            'Как пустой универсам!')
        self.assertEqual(
            how_you_doing(
                'как сам zzz ?',
                ['Как пустой универсам!']),
            None)

    def test_is_good(self):
        self.assertEqual(is_good('тест тест тест'), False)
        self.assertEqual(is_good('Вчера мамку твою послал'), True)
        self.assertEqual(is_good('Вчера МАМКУ твою послал'), True)
        self.assertEqual(is_good('радуйся что не с твоей мамкой'), True)
        self.assertEqual(is_good('радуйся что не с твоим анусом'), True)
        self.assertEqual(
            is_good(
                'твоя мамаша настолько жирная, что не помещается в панорамный режим'),
            True)
        self.assertEqual(
            is_good(
                'Твоя мама такая толстая, что она плавала в окене и все принимали ее за новый континет!'),
            True)

    def test_is_plan(self):
        self.assertEqual(is_plan('Уже давно всё на го переписали'), False)
        self.assertEqual(is_plan('Давайте всё на го перепишем'), True)

    def test_fag_replay(self):
        self.assertEqual(fag_reply('asdlfajsldf'), None)
        self.assertEqual(fag_reply('нет'), 'Пидора ответ!')
        self.assertEqual(fag_reply('нет.'), 'Пидора ответ!')
        self.assertEqual(fag_reply('eng HET'), 'Пидора ответ!')
        self.assertEqual(fag_reply('н е т'), 'Пидора ответ!')
        self.assertEqual(fag_reply('н Е    т'), 'Пидора ответ!')
        self.assertEqual(fag_reply('aa нет'), 'Пидора ответ!')
        self.assertEqual(fag_reply('aa НЕТ  '), 'Пидора ответ!')
        self.assertEqual(fag_reply('aa НЕТ !!?? '), 'Пидора ответ!')
        self.assertEqual(fag_reply('нет ты'), None)


if __name__ == '__main__':
    unittest.main()
