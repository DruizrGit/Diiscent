from fractions import Fraction
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.style.use('ggplot')

class AttackPool:
    
    def __init__(self):
        """
        Terminology:
        - Event: Given a collection of dice, an event describes a possible roll outcome in terms of number of hearts, range and surges.
        - Bundle: A bundle is an event, taken together with its associated probability.
        """
        
        self.event_keys = ['Heart', 'Range', 'Surge']
        self.atk_colours = ['Red','Yellow','Blue','Green']
        self.atk_state = {'Red': 0,
                      'Yellow': 0,
                      'Blue': 0,
                      'Green':0
                      }
        
        self.heart_max ={'Red': 3,
                         'Blue': 2,
                         'Yellow': 2,
                         'Green':1
                         }
        
        self.range_max ={'Red': 0,
                         'Blue': 6,
                         'Yellow': 2,
                         'Green': 1
                         }
        self.heart_min = {'Red': 1,
                         'Blue': 1,
                         'Yellow': 0,
                         'Green':0
                         }
        self.range_min = {'Red': 0,
                          'Blue': 2,
                          'Yellow': 0,
                          'Green': 0            
                          }
                
        self.red_die = [{'Heart': 1, 'Range': 0, 'Surge': 0, 'Prob': Fraction(1,6)},
                     {'Heart': 2, 'Range': 0, 'Surge': 0, 'Prob': Fraction(1,2)},
                     {'Heart': 3, 'Range': 0, 'Surge': 0, 'Prob': Fraction(1,6)},
                     {'Heart': 3, 'Range': 0, 'Surge': 1, 'Prob': Fraction(1,6)}
                     ]
        
        self.blue_die = [{'Heart': 'Miss', 'Range': 'Miss', 'Surge': 'Miss', 'Prob': Fraction(1,6)},
                     {'Heart': 1, 'Range': 5, 'Surge': 0, 'Prob': Fraction(1,6)},
                     {'Heart': 1, 'Range': 6, 'Surge': 1, 'Prob': Fraction(1,6)},
                     {'Heart': 2, 'Range': 2, 'Surge': 1, 'Prob': Fraction(1,6)},
                     {'Heart': 2, 'Range': 3, 'Surge': 0, 'Prob': Fraction(1,6)},
                     {'Heart': 2, 'Range': 4, 'Surge': 0, 'Prob': Fraction(1,6)}
                    ]
        
        self.yellow_die = [{'Heart': 0, 'Range': 1, 'Surge': 1, 'Prob': Fraction(1,6)},
                     {'Heart': 1, 'Range': 1, 'Surge': 0, 'Prob': Fraction(1,6)},
                     {'Heart': 1, 'Range': 2, 'Surge': 0, 'Prob': Fraction(1,6)},
                     {'Heart': 1, 'Range': 0, 'Surge': 1, 'Prob': Fraction(1,6)},
                     {'Heart': 2, 'Range': 0, 'Surge': 0, 'Prob': Fraction(1,6)},
                     {'Heart': 2, 'Range': 0, 'Surge': 1, 'Prob': Fraction(1,6)}
                    ]
        
        self.green_die = [{'Heart': 0, 'Range': 0, 'Surge': 1, 'Prob': Fraction(1,6)},
                     {'Heart': 0, 'Range': 1, 'Surge': 1, 'Prob': Fraction(1,6)},
                     {'Heart': 1, 'Range': 0, 'Surge': 0, 'Prob': Fraction(1,6)},
                     {'Heart': 1, 'Range': 1, 'Surge': 0, 'Prob': Fraction(1,6)},
                     {'Heart': 1, 'Range': 0, 'Surge': 1, 'Prob': Fraction(1,6)},
                     {'Heart': 1, 'Range': 1, 'Surge': 1, 'Prob': Fraction(1,6)}
                    ]
        
        self.dice = {'Red': self.red_die, 
                     'Yellow': self.yellow_die,
                     'Blue': self.blue_die,
                     'Green': self.green_die
                     }
        
    def roll(self):
        
        dice = []
        
        for colour in self.atk_colours:
            for num_die in range(self.atk_state[colour]):
                dice.append(self.dice[colour])
                
        total_bundle = dice[0]   
        
        for die in dice[1::]:
            
            total_bundle = self.bundle_combine(total_bundle,die)
            
        return total_bundle
        
    def bundle_combine(self, bundle_A, bundle_B):
        
        # Not strictly just single dice. Combines two object events such as 
        # 1) Collection of two dice and 
        # 2) a (third) independent die
        bundles = []
        events = []
        
        for bundle_a in bundle_A:
                
            for bundle_b in bundle_B:
                
                if bundle_a['Heart'] == 'Miss' or bundle_b['Heart'] == 'Miss':
                    new_bundle = {'Heart': 'Miss', 'Range': 'Miss', 'Surge': 'Miss', 'Prob': bundle_a['Prob']*bundle_b['Prob']}
                    new_event = {'Heart': 'Miss', 'Range': 'Miss', 'Surge': 'Miss'}
                    
                else:
                    new_bundle = self.combine_bundles(bundle_a, bundle_b)
                    new_event = self.grab_event(new_bundle)
                
                if new_event in events:
                    bundles[self.iloc_bundle_match(bundles, new_event)]['Prob'] += new_bundle['Prob']
                else:
                    events.append(new_event)
                    bundles.append(new_bundle)
                    
        return bundles
                
    def iloc_bundle_match(self, bundles, target):
        iloc = 0
        
        for bundle in bundles:
            
            if self.grab_event(bundle) == target:
        
                return iloc
            else:
                iloc+=1
                
    
    def combine_bundles(self, bundle_1, bundle_2):
        
        combined_bundle = {'Heart': bundle_1['Heart'] + bundle_2['Heart'],
                 'Range': bundle_1['Range'] + bundle_2['Range'],
                 'Surge': bundle_1['Surge'] + bundle_2['Surge'],
                 'Prob': bundle_1['Prob']*bundle_2['Prob']
                 }
        
        return combined_bundle
    
    def event_select(self, heart_val=0, range_val = 0, surge_val = 0, heart_measure = 'great', range_measure = 'great', surge_measure = 'great'):
        
        events = []
        
        if heart_val == 'Miss':
            
            for event in self.roll():
                if event['Heart'] == 'Miss':
                    events.append(event)
        else:      
            
            for event in self.roll():
                
                if event['Heart'] != 'Miss': 
                    
                    if self.event_comparison(event['Heart'], heart_val, heart_measure) and self.event_comparison(event['Range'], range_val, range_measure) and self.event_comparison(event['Surge'], surge_val, surge_measure):
                        
                        events.append(event)
                else:
                    pass
                
        bundle = {'Events': events, 
                  'Prob': self.prob_measure(events)}
        
        return bundle
                        
    def event_comparison(self, event_val, value, measure):
        
        if measure == 'exact':
            
            if event_val == value:
                return True
            else:
                return False
            
        elif measure == 'great':
            
            if event_val >= value:
                return True
            else:
                return False
            
        else:
            
            if event_val <= value:
                return True
            else:
                
                return False
                  
    def prob_measure(self, events):
        
        # Provides the total probability for a selection of events
        prob = 0
        
        for event in events:
            
            prob += event['Prob']
            
        return prob
    
    def grab_event(self, event):
        
        keys = ['Heart', 'Range', 'Surge']
        
        return {key: event[key] for key in keys}
        
    def max_heart(self):
        
        m_heart = 0
        for colour in self.atk_colours:
            m_heart += self.heart_max[colour]*self.atk_state[colour]
            
        return m_heart
     
    def max_range(self):
        
        m_range = 0
        for colour in self.atk_colours:
            m_range += self.range_max[colour]*self.atk_state[colour]
            
        return m_range
    
    def fraction_rounder(self,fraction):
    
        numer = fraction.numerator
        denom = fraction.denominator
        value = numer/denom
        
        if 0.1 <= value and value < 1:
            return round(value,1)
        elif 0.01 <= value and value < 0.1:
            return round(value, 2)
        elif 0.001 <= value and value < 0.01:
            return round(value, 3)
        else:
            return round(value)

    def atk_plot(self, kind = 'Heart', measure = 'great'):
 
        probs = []
        
        if measure == 'exact':
                str_kind = 'exactly'
        elif measure == 'great':
            str_kind = 'at least'
        else:
            str_kind = 'less than'
                
        if kind == 'Heart':
            
            maxh = self.max_heart()

            # Construct Values and Include Misses (if necessary)
            if self.atk_state['Blue'] != 0:
                probs.append(self.event_select('Miss')['Prob']*100)
                
                # Construct Values
                x_axis = [i for i in range(maxh+2)]
                values = [i-1 for i in range(maxh+2)]
                values[0] = 'Miss'
            else:
                x_axis = [i for i in range(maxh+1)]
                values= [str(i) for i in range(maxh+1)]
                
            for val in range(maxh+1):
                probs.append(self.event_select(heart_val = val, heart_measure = measure)['Prob']*100)
            
            print(values)
            print(probs)
            
            bar = plt.bar(x = x_axis, height = probs)
            ind = 0
            
            for rect in bar:
                height = rect.get_height()
                plt.text(rect.get_x() + rect.get_width()/2, height, str(self.fraction_rounder(probs[ind])) + "%", 
                         ha = 'center', va = 'bottom', size = 8)
                ind+=1
            
            plt.xlabel('Hearts')
            plt.ylabel('Probability (%)')
            plt.xticks(x_axis, values)    
            plt.title('Probability of Rolling ' + str_kind + ' X Hearts', y = 1.08)
            plt.ylim(0,100)
            plt.show()
            
        else:
            
            maxr = self.max_range()

            if self.atk_state['Blue'] != 0:
                probs.append(self.event_select(heart_val = 'Miss')['Prob']*100)
                
                # Construct Values
                x_axis = [i for i in range(maxr+2)]
                values = [i-1 for i in range(maxr+2)]
                values[0] = 'Miss'
            else:
                x_axis = [i for i in range(maxr+1)]
                values= [str(i) for i in range(maxr+1)]
                
            for val in range(maxr+1):
                probs.append(self.event_select(range_val = val, range_measure = measure)['Prob']*100)
            
            print(values)
            print(probs)

            bar = plt.bar(x = x_axis, height = probs)
            ind = 0
            
            for rect in bar:
                height = rect.get_height()
                plt.text(rect.get_x() + rect.get_width()/2, height, str(self.fraction_rounder(probs[ind])) + "%", ha = 'center', va = 'bottom', 
                         size = 8)
                ind+=1
            
            plt.xlabel('Range')
            plt.ylabel('Probability (%)')
            plt.xticks(x_axis, values)
            plt.title('Probability of Rolling ' + str_kind + ' X Range', y = 1.08)
            plt.ylim(0,100)
            plt.show()
              
class DefensePool:
    
    def __init__(self):
        """
        Terminology:
        - Event: Given a collection of dice, an event describes a possible roll outcome in terms of number of hearts, range and surges.
        - Bundle: A bundle is an event, taken together with its associated probability.
        """
        
        self.def_colours = ['Black', 'Grey', 'Brown']
        self.event_keys = ['Shield']
        
        self.def_state = {'Black': 0,
                          'Grey': 0,
                          'Brown': 0
                          }
        
        self.black_die =  [{'Shield': 0, 'Prob': Fraction(1,6)},
                           {'Shield': 2, 'Prob': Fraction(1,2)},
                           {'Shield': 3, 'Prob': Fraction(1,6)},
                           {'Shield': 4, 'Prob': Fraction(1,6)}
                           ]
        
        self.grey_die =  [{'Shield': 0, 'Prob': Fraction(1,6)},
                          {'Shield': 1, 'Prob': Fraction(1,2)},
                          {'Shield': 2, 'Prob': Fraction(1,6)},
                          {'Shield': 3, 'Prob': Fraction(1,6)}
                          ]
        
        self.brown_die =  [{'Shield': 0, 'Prob': Fraction(1,2)},
                           {'Shield': 1, 'Prob': Fraction(1,3)},
                           {'Shield': 2, 'Prob': Fraction(1,6)}
                           ]
        
        self.shield_max = {'Black': 4,
                           'Grey': 3,
                           'Brown': 2
                           }
        
        self.dice = {'Black': self.black_die,
                     'Grey': self.grey_die,
                     'Brown': self.brown_die
                    }
        
    def roll(self):
        
        dice = []
        
        for colour in self.def_colours:
            for num_die in range(self.def_state[colour]):
                dice.append(self.dice[colour])
                
        total_bundle = dice[0]   
        
        for die in dice[1::]:
            
            total_bundle = self.bundle_combine(total_bundle,die)
            
        return total_bundle
        
    def bundle_combine(self, bundle_A, bundle_B):
        
        # Not strictly just single dice. Combines two object events such as 
        # 1) Collection of two dice and 
        # 2) a (third) independent die
        bundles = []
        events = []
        
        for bundle_a in bundle_A:
                
            for bundle_b in bundle_B:
                
                new_bundle = self.combine_bundles(bundle_a, bundle_b)
                new_event = self.grab_event(new_bundle)
                
                if new_event in events:
                    bundles[self.iloc_bundle_match(bundles, new_event)]['Prob'] += new_bundle['Prob']
                else:
                    events.append(new_event)
                    bundles.append(new_bundle)
                    
        return bundles
                
    def iloc_bundle_match(self, bundles, target):
        iloc = 0
        
        for bundle in bundles:
            
            if self.grab_event(bundle) == target:
        
                return iloc
            else:
                iloc+=1
                
    def combine_bundles(self, bundle_1, bundle_2):
        # Adds 2 Independent Bundles together
        
        combined_bundle = {'Shield': bundle_1['Shield'] + bundle_2['Shield'],
                 'Prob': bundle_1['Prob']*bundle_2['Prob']
                 }
        
        return combined_bundle
    
    def grab_event(self, event):
        
        return {'Shield': event['Shield']}
    
    def event_select(self, shield_val, shield_measure = 'great'):
        
        events = []

        for event in self.roll():
                
            if self.event_comparison(event['Shield'], shield_val, shield_measure):
                events.append(event)

                
        bundle = {'Events': events, 
                  'Prob': self.prob_measure(events)}
        
        return bundle
                        
    def event_comparison(self, event_val, value, measure):
        
        if measure == 'exact':
            
            if event_val == value:
                return True
            else:
                return False
            
        elif measure == 'great':
            
            if event_val >= value:
                return True
            else:
                return False
            
        else:
            
            if event_val <= value:
                return True
            else:
                
                return False
            
    def fraction_rounder(self,fraction):
    
        numer = fraction.numerator
        denom = fraction.denominator
        value = numer/denom
        
        if 0.1 <= value and value < 1:
            return round(value,1)
        elif 0.01 <= value and value < 0.1:
            return round(value, 2)
        elif 0.001 <= value and value < 0.01:
            return round(value, 3)
        else:
            return round(value)
        
    def max_shield(self):
            
        total = 0
        for colour in self.def_colours:
            total += self.def_state[colour]*self.shield_max[colour]
        
        return total
    
    def prob_measure(self, events):
        
        prob = 0
        
        for event in events:
            
            prob += event['Prob']
            
        return prob










