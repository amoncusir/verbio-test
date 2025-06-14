from src.app.utils import Singleton


# Create a class that uses the Singleton metaclass
class MySingletonClass(metaclass=Singleton):
    def __init__(self, value):
        self.value = value

    @classmethod
    def remove_instance(cls):
        Singleton.remove_instance(cls)


def test_single_instance():
    """
    Test that multiple instances of the singleton class refer to the same object.
    """

    MySingletonClass.remove_instance()

    # First instance creation
    instance1 = MySingletonClass(10)

    # Second instance creation
    instance2 = MySingletonClass(20)

    # Assert both instances are the same
    assert instance1 is instance2


def test_instance_retains_initial_value():
    """
    Test that the second initialization does not override the singleton's attributes.
    """

    MySingletonClass.remove_instance()

    # First instance creation
    instance1 = MySingletonClass(30)

    # Create another instance
    instance2 = MySingletonClass(40)

    # Ensure both instances are the same
    assert instance1 is instance2

    # Check if the value from the first initialization remains intact
    assert instance1.value == 30
    assert instance2.value == 30


def test_singleton_persists_across_calls():
    """
    Test that the singleton persists across different calls.
    """

    MySingletonClass.remove_instance()

    # Initial instance creation
    instance1 = MySingletonClass(50)

    # Later in the code, retrieve the instance again
    instance2 = MySingletonClass(60)

    # Assert both instances are still the same
    assert instance1 is instance2

    # Ensure the initial state is preserved
    assert instance1.value == 50


def test_different_classes():
    """
    Test that different classes with the Singleton metaclass have separate instances.
    """

    class AnotherSingletonClass(metaclass=Singleton):
        def __init__(self, value):
            self.value = value

    MySingletonClass.remove_instance()

    instance1 = MySingletonClass(100)
    instance2 = AnotherSingletonClass(200)

    # They should not be the same instance because they are different classes
    assert instance1 is not instance2

    # Assert the values are as expected
    assert instance1.value == 100
    assert instance2.value == 200


def test_remove_instance():
    """
    Test that removing an instance allows the Singleton class to create a new instance.
    """
    # Create initial instance
    instance1 = MySingletonClass(10)

    # Remove the instance
    Singleton.remove_instance(MySingletonClass)

    # Create a new instance, this should be a different object
    instance2 = MySingletonClass(20)

    # Check that the new instance is not the same as the old one
    assert instance1 is not instance2
    assert instance2.value == 20


def test_remove_instance_no_effect_on_others():
    """
    Test that removing an instance of one class doesn't affect the singleton instances of other classes.
    """

    class AnotherSingletonClass(metaclass=Singleton):
        def __init__(self, value):
            self.value = value

    # Create instances for both classes
    instance1 = MySingletonClass(100)
    instance2 = AnotherSingletonClass(200)

    # Remove instance from MySingletonClass
    MySingletonClass.remove_instance()

    # Create a new instance for MySingletonClass, should be a new object
    instance3 = MySingletonClass(300)

    # Ensure that instance2 for AnotherSingletonClass is unaffected
    assert instance2.value == 200

    # Check the new instance for MySingletonClass
    assert instance1 is not instance3
    assert instance3.value == 300


def test_bypass_singleton():
    """
    Test that the singleton can be bypassed when the bypass_singleton flag is set.
    """

    # Remove instance from MySingletonClass
    MySingletonClass.remove_instance()

    # First instance created normally
    instance1 = MySingletonClass(10)

    # Second instance bypasses the singleton
    instance2 = MySingletonClass(20, bypass_singleton=True)

    # Verify that they are not the same instance
    assert instance1 is not instance2

    # Ensure that the second instance has the correct value
    assert instance2.value == 20


def test_bypass_singleton_no_effect_on_singleton_instance():
    """
    Test that bypassing singleton does not affect the original singleton instance.
    """

    # Remove instance from MySingletonClass
    MySingletonClass.remove_instance()

    # First instance created normally
    instance1 = MySingletonClass(10)

    # Second instance bypasses the singleton
    instance2 = MySingletonClass(20, bypass_singleton=True)  # noqa: F841

    # Third instance without bypass should return the original singleton
    instance3 = MySingletonClass(30)

    # Check that the original singleton instance is returned for instance3
    assert instance1 is instance3

    # The value should remain unchanged for the original singleton
    assert instance1.value == 10
