import unittest
from anikattu.keyedlist import KeyedList


class KeyedListTest(unittest.TestCase):

    def setUp(self):
        self.testlist = KeyedList({
            
            'model': {
                'module_lstm': {
                    'hidden_dim': 200,
                    'embed_dim' : 100,
                },
                
                'module_conv': {
                    'padding' : 2,
                    'stride'  : 2,
                    'height'  : 4,
                'width'   : 3,
                }
            },
            
            'training_config' : {
                'batch_size'    : 20,
                'epochs'        : 200,
                'learning_rate' : 1e-4,
                
            },

        
        })

    def tearDown(self):
        pass

    def test_access(self):
        self.assertEqual(self.testlist['model.module_lstm.hidden_dim'], 200)
        self.assertEqual(self.testlist['model.module_lstm.embed_dim'], 100)

        self.assertEqual(self.testlist['model.module_conv.stride'], 2)
        
    def test_deletion(self):
        del self.testlist['model.module_lstm.hidden_dim']
        with self.assertRaises(KeyError):
            self.testlist['model.module_lstm.hidden_dim']
            
            
        self.testlist['model.module_lstm.hidden_dim'] = 300
        self.assertEqual(self.testlist['model.module_lstm.hidden_dim'], 300)


    def test_value_change(self):
        self.testlist['testing_config'] =30

        with self.assertRaises(KeyError):
            self.testlist['testing_config.value'] = 300

        
        del self.testlist['testing_config']
        self.testlist['testing_config.value'] = 500
        self.assertEqual(self.testlist['testing_config.value'], 500)

        self.testlist['testing_config.batch_size'] = 50
        self.assertEqual(self.testlist['testing_config.batch_size'], 50)


if __name__ == '__main__':
    unittest.main()
