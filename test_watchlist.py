import unittest
from app import app, db, Movie, User, forge, initdb

class WatchlistTestcase(unittest.TestCase):

    def setUp(self):
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'
        )
        db.create_all()
        user = User(name='Test', username='test')
        user.set_password('123')
        movie = Movie(title='Test Movie Title', year='2020')
        db.session.add_all([user, movie])
        db.session.commit()
        self.client = app.test_client()
        self.runner = app.test_cli_runner()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_app_exist(self):
        self.assertIsNotNone(app)

    def test_app_is_testing(self):
        self.assertTrue(app.config['TESTING'])

    def test_404_page(self):
        response = self.client.get('/nothing')
        data = response.get_data(as_text=True)
        self.assertIn('Page Not Found - 404', data)
        self.assertIn('Go Back', data)
        self.assertEqual(response.status_code, 404)

    def test_index_page(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertIn('Test\'s Watchlist', data)
        self.assertIn('Test Movie Title', data)
        self.assertEqual(response.status_code, 200)

    def login(self):
        self.client.post('/login', data=dict(
            username='test',
            password='123'
        ), follow_redirects=True)

    def test_create_item(self):
        self.login()
        response = self.client.post('/', data=dict(
            title='New Movie',
            year='2020'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('加好了捏.', data)
        self.assertIn('New Movie', data)

        response = self.client.post('/', data=dict(
            title='',
            year='2020'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('加好了捏.', data)
        self.assertIn('谋法加入.', data)

        response = self.client.post('/', data=dict(
            title='New Movie',
            year=''
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('加好了捏.', data)
        self.assertIn('谋法加入.', data)

    def test_update_item(self):
        self.login()

        # test update item
        response = self.client.get('/movie/edit/1')
        data = response.get_data(as_text=True)
        self.assertIn('Edit item', data)
        self.assertIn('Test Movie Title', data)
        self.assertIn('2020', data)
        self.assertEqual(response.status_code, 200)

        # test update item with valid data
        response = self.client.post('/movie/edit/1', data=dict(
            title='New Movie',
            year='2020'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('加好了捏.', data)
        self.assertIn('New Movie', data)
        self.assertEqual(response.status_code, 200)

        # test update item with invalid data
        response = self.client.post('/movie/edit/1', data=dict(
            title='',
            year='2020'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('加好了捏.', data)
        self.assertIn('Invalid input.', data)

        # test update item with invalid data
        response = self.client.post('/movie/edit/1', data=dict(
            title='New Movie',
            year=''
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('加好了捏.', data)
        self.assertIn('Invalid input.', data)

    def test_delete_item(self):
        self.login()

        response = self.client.post('/movie/delete/1', follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('扔垃圾桶了捏.', data)
        self.assertNotIn('Test Movie Title', data)
    
    def test_forge_command(self):
        result = self.runner.invoke(forge)
        self.assertIn('Done.', result.output)
        self.assertNotEqual(Movie.query.count(), 0)
    
    def test_initdb_command(self):
        result = self.runner.invoke(initdb)
        self.assertIn('Initialising database.', result.output)

    def test_admin_command(self):
        db.drop_all()
        db.create_all()
        result = self.runner.invoke(args=['admin', '--username', 'test', '--password', '123'])
        self.assertIn('Creating user...', result.output)
        self.assertIn('Done.', result.output)
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(User.query.first().username, 'test')
        self.assertTrue(User.query.first().validate_password('123'))

    def test_admin_command_update(self):
        result = self.runner.invoke(args=['admin', '--username', 'peter', '--password', '456'])
        self.assertIn('Updating user...', result.output)
        self.assertIn('Done.', result.output)
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(User.query.first().username, 'peter')
        self.assertTrue(User.query.first().validate_password('456'))

if __name__ == '__main__':
    unittest.main()
