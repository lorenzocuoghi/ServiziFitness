import React, { Component } from 'react';
import { FlatList, StyleSheet, Text, View } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import Ionicons from 'react-native-vector-icons/Ionicons';

class TrainingCardListScreen extends Component {
  constructor(props) {
      super(props);

      this.state = {
        card_list: [],
        isLoading: true,
      };
  };

  componentDidMount() {
    fetch('http://127.0.0.1:8000/workout/api/trainingcard/search/')
      .then((response) => response.json())
      .then((json) => {
        this.setState({ card_list: json });
        console.log({ json });
      })
      .catch((error) => console.error(error))
      .finally(() => {
        this.setState({ isLoading: false });
      });
  }

  render () {
    const renderItem = ({ item }) => (
      <View style={styles.item}>
        <Text style={styles.title}>{item.name}</Text>
      </View>
    );

    return (
      <View style={styles.container}>
        <FlatList
          data={this.state.card_list}
          renderItem={renderItem}
          keyExtractor={item => item.id}
      />
      </View>
    );
  }
}

class TrainingCardDetailScreen extends Component {
  render () {
    return (
      <View style={styles.container}>
        <Text>Training Card</Text>
      </View>
    );
  }
}

class ExerciseListScreen extends Component {
  render () {
    return (
      <View style={styles.container}>
        <Text>Exercises</Text>
      </View>
    );
  }
}

class ExerciseDetailScreen extends Component {
  render () {
    return (
      <View style={styles.container}>
        <Text>Exercise</Text>
      </View>
    );
  }
}

class ProfileScreen extends Component {
  render () {
    return (
      <View style={styles.container}>
        <Text>Profile</Text>
      </View>
    );
  }
}

const TrainingCardStack = createStackNavigator();

function TrainingCardStackScreen() {
  return (
    <TrainingCardStack.Navigator>
      <TrainingCardStack.Screen name="Training Card List" component={TrainingCardListScreen} />
      <TrainingCardStack.Screen name="Training Card Detail" component={TrainingCardDetailScreen} />
    </TrainingCardStack.Navigator>
  );
}

const ExerciseStack = createStackNavigator();

function ExerciseStackScreen() {
  return (
    <ExerciseStack.Navigator>
      <ExerciseStack.Screen name="Exercise List" component={ExerciseListScreen} />
      <ExerciseStack.Screen name="Exercise Detail" component={ExerciseDetailScreen} />
    </ExerciseStack.Navigator>
  );
}

const Tab = createBottomTabNavigator();

export default class ServiziFitnessApp extends Component {
  constructor(props) {
    super(props);

    this.state = {
      data: [],
      isLoading: true,
    };
  }

  componentDidMount() {
    fetch('http://127.0.0.1:8000/workout/api/exercise/search/1/')
      .then((response) => response.json())
      .then((json) => {
        this.setState({ data: json });
        console.log({ json });
      })
      .catch((error) => console.error(error))
      .finally(() => {
        this.setState({ isLoading: false });
      });
  }

  render() {
    const { data, isLoading } = this.state;

    return (
      <NavigationContainer>
        <Tab.Navigator
          screenOptions={({ route }) => ({
            tabBarIcon: ({ focused, color, size }) => {
              let iconName;
  
              if (route.name === 'Training Cards') {
                iconName = focused ? 'clipboard' : 'clipboard-outline';
              } else if (route.name === 'Exercises') {
                iconName = focused ? 'ios-barbell' : 'ios-barbell-outline';
              } else if (route.name === 'Profile') {
                iconName = focused ? 'person' : 'person-outline';
              }
  
              return <Ionicons name={iconName} size={size} color={color} />;
            },
          })}
          tabBarOptions={{
            activeTintColor: 'blue',
            inactiveTintColor: 'gray',
          }}
        >
          <Tab.Screen name="Training Cards" component={TrainingCardStackScreen} />
          <Tab.Screen name="Exercises" component={ExerciseStackScreen} />
          <Tab.Screen name="Profile" component={ProfileScreen} />
        </Tab.Navigator>
      </NavigationContainer>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});
