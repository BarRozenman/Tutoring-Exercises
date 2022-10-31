import copy
import itertools
import matplotlib.pyplot as plt
import numpy as np

'''
finding the most efficient route from top left of a random matrix.

Create a 100X100 matrix with values that represent elevation, 
Move from the top right corner to the bottom left corner while trying to conserve as much Energy as possible.
Energy is 1*descending or 2* ascending for each step
'''

np.random.seed(77)  # establishing constant randomization
mat = np.random.random((100, 100))
current_location = np.array([0, 0])
end = np.array([99, 99])
x = np.linspace(-1, 1, 3)
y = np.linspace(-1, 1, 3)
diff = np.array(list(itertools.product(x, y))).astype(int)  # all possible moves
diff = np.delete(diff, 4, 0)  # removing the [0,0] element
been_to = copy.deepcopy(current_location)[None, :]
count = -1
good_direction_idx = [-1, -2, -4]  # the best direction to move in
sum_energy = 0  # the total energy used
base_step_energy_cost = 0.3  
while not np.array_equal(end, current_location):  # while not at the end
    count += 1
    optionals_locations = current_location + diff
    optionals_locations[optionals_locations < 0] = 0  # making sure we don't go out of bounds
    optionals_locations[optionals_locations >= len(mat)] = len(mat) - 1  # making sure we don't go out of bounds
    current_elevation = mat[current_location[0], current_location[1]]
    optionals_elev = mat[optionals_locations[:, 0], optionals_locations[:, 1]]  # the elevation of the possible moves
    energy = current_elevation - optionals_elev  # the energy used for each move
    energy[good_direction_idx] = energy[good_direction_idx] - 0.1  # making the best moves a little better
    energy[energy > 0] = energy[energy > 0] * 2  # making the energy for ascending moves twice as much
    energy[energy < 0] = np.abs(
        energy[energy < 0])  # making the energy for descending moves positive (no such thing as negative energy)
    energy = energy + base_step_energy_cost # adding the base step energy cost
    order = np.argsort(energy)  # sorting the energy from least to greatest
    if count > 1000:  # if we've been going in circles for too long stop the while loop
        break
    for i in order:  # going through the possible moves in order of the least energy used
        if not any(np.equal(been_to, optionals_locations[i, :]).all(1)):  # if we haven't been to this location before
            current_location = optionals_locations[i, :]  # move to this location
            been_to = np.vstack((been_to, current_location))  # add this location to the list of locations we've been to
            print(f'current location is: {current_location}')
            sum_energy += energy[i]  # add the energy used to the total energy used
            break
        elif current_location[0] == 99:  # if we're at the bottom of the matrix
            current_location = optionals_locations[-4, :]
            been_to = np.vstack((been_to, current_location))
            sum_energy += energy[i]
            print(f'current location is: {current_location}')
            break
        elif current_location[1] == 99:  # if we're on the right side of the matrix
            current_location = optionals_locations[-2, :]
            been_to = np.vstack((been_to, current_location))
            sum_energy += energy[i]
            print(f'current location is: {current_location}')
            break
        else:  # if we've been to all the possible locations for this step
            current_location = optionals_locations[-1, :]
            been_to = np.vstack((been_to, current_location))
            sum_energy += energy[i]
            print(f'current location is: {current_location}')
            break

route_visualization = np.zeros((100, 100))
route_visualization[
    been_to[:, 0], been_to[:, 1]] = 255  # creating a visualization of the route for all the locations we've been to
plt.title(f'total_energy: {sum_energy}')
plt.imshow(route_visualization, cmap='gray')
plt.show()
