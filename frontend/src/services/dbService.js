// This is a mock database service. In a real app, you would connect to your backend API
const users = JSON.parse(localStorage.getItem('users') || '[]');

export const dbService = {
  // Check if user exists
  async findUser(username) {
    return users.find(user => user.username === username);
  },

  // Add new user
  async addUser(username, password) {
    if (await this.findUser(username)) {
      throw new Error('Username already exists');
    }
    
    const newUser = {
      username,
      password, // In a real app, this should be hashed
      createdAt: new Date().toISOString()
    };
    
    users.push(newUser);
    localStorage.setItem('users', JSON.stringify(users));
    localStorage.setItem('email', username);
    localStorage.setItem('password', password);
    return newUser;
  },

  // Verify user credentials
  async verifyUser(username, password) {
    const user = await this.findUser(username);
    if (!user || user.password !== password) {
      throw new Error('Invalid username or password');
    }
    return user;
  }
}; 