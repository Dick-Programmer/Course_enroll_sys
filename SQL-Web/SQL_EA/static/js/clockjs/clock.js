// 检查是否为对象类的实例
function _classCallCheck(instance, Constructor) {
	if (!(instance instanceof Constructor)) {
		throw new TypeError("不能加载方法！"); 
	} 
}

// 构造函数返回
function _possibleConstructorReturn(self, call) { 
	if (!self) { 
		throw new ReferenceError("还没有初始化——super()没有被调用。"); 
	} 
	return call && (typeof call === "object" || typeof call === "function") ? call : self; 
}

// 继承
function _inherits(subClass, superClass) { 
	if (typeof superClass !== "function" && superClass !== null) {
		throw new TypeError("表达式要么是null，要么是函数，而不是" + typeof superClass); 
	} 
	subClass.prototype = Object.create(superClass && superClass.prototype, {
		constructor: {
			value: subClass, enumerable: false, writable: true, configurable: true 
		} 
	}); 
	if (superClass) 
		Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; 
}

// 动画卡
var AnimatedCard = function (_React$Component) {
	_inherits(AnimatedCard, _React$Component);

	function AnimatedCard() {
		_classCallCheck(this, AnimatedCard);

		return _possibleConstructorReturn(this, _React$Component.apply(this, arguments));
	}

	AnimatedCard.prototype.render = function render() {
		var _props = this.props;
		var position = _props.position;
		var digit = _props.digit;
		var animation = _props.animation;

		return React.createElement(
			'div',
			{ className: 'flipCard ' + position + ' ' + animation },
			React.createElement(
				'span',
				null,
				digit
			)
		);
	};

	return AnimatedCard;
}(React.Component);

// 静态元素
var StaticCard = function (_React$Component2) {
	_inherits(StaticCard, _React$Component2); // 

	function StaticCard() {
		_classCallCheck(this, StaticCard);

		return _possibleConstructorReturn(this, _React$Component2.apply(this, arguments));
	}

	StaticCard.prototype.render = function render() {
		var _props2 = this.props;
		var position = _props2.position;
		var digit = _props2.digit;

		return React.createElement(
			'div',
			{ className: position },
			React.createElement(
				'span',
				null,
				digit
			)
		);
	};
	return StaticCard;
}(React.Component);

// 翻转单元容器
var FlipUnitContainer = function (_React$Component3) {
	_inherits(FlipUnitContainer, _React$Component3);

	function FlipUnitContainer() {
		_classCallCheck(this, FlipUnitContainer);
		return _possibleConstructorReturn(this, _React$Component3.apply(this, arguments));
	}

	FlipUnitContainer.prototype.render = function render() {
		var _props3 = this.props;
		var digit = _props3.digit;
		var shuffle = _props3.shuffle;
		var unit = _props3.unit;

		var now = digit;
		var before = digit - 1;

		// 防止出现负值
		if (unit !== 'hours') {
			before = before === -1 ? 59 : before;
		} else {
			before = before === -1 ? 23 : before;
		}

		// 补0
		if (now < 10) now = '0' + now;
		if (before < 10) before = '0' + before;

		// 随机数字
		var digit1 = shuffle ? before : now;
		var digit2 = !shuffle ? before : now;

		// 随机动画
		var animation1 = shuffle ? 'fold' : 'unfold';
		var animation2 = !shuffle ? 'fold' : 'unfold';

		return React.createElement(
			'div',
			{ className: 'flipUnitContainer' },
			React.createElement(StaticCard, {
				position: 'upperCard',
				digit: now
			}),
			React.createElement(StaticCard, {
				position: 'lowerCard',
				digit: before
			}),
			React.createElement(AnimatedCard, {
				position: 'first',
				digit: digit1,
				animation: animation1
			}),
			React.createElement(AnimatedCard, {
				position: 'second',
				digit: digit2,
				animation: animation2
			})
		);
	};

	return FlipUnitContainer;
}(React.Component);

// 翻页时钟
var FlipClock = function (_React$Component4) {
	_inherits(FlipClock, _React$Component4); // 继承

	function FlipClock(props) {
		_classCallCheck(this, FlipClock); 

		var _this4 = _possibleConstructorReturn(this, _React$Component4.call(this, props));

		_this4.state = {
			hours: 0,
			hoursShuffle: true,
			minutes: 0,
			minutesShuffle: true,
			seconds: 0,
			secondsShuffle: true
		};
		return _this4;
	}

	FlipClock.prototype.componentDidMount = function componentDidMount() {
		var _this5 = this;

		this.timerID = setInterval(function () {
			return _this5.updateTime();
		}, 50);
	};

	FlipClock.prototype.componentWillUnmount = function componentWillUnmount() {
		clearInterval(this.timerID);
	};

	FlipClock.prototype.updateTime = function updateTime() {
		// 日期
		var time = new Date();
		// 时间
		var hours = time.getHours();
		var minutes = time.getMinutes();
		var seconds = time.getSeconds();
		// 在小时改变时，更新this.state.hours
		if (hours !== this.state.hours) {
			var hoursShuffle = !this.state.hoursShuffle;
			this.setState({
				hours: hours,
				hoursShuffle: hoursShuffle
			});
		}
		// 在分钟改变时，更新 this.state.minutes
		if (minutes !== this.state.minutes) {
			var minutesShuffle = !this.state.minutesShuffle;
			this.setState({
				minutes: minutes,
				minutesShuffle: minutesShuffle
			});
		}
		// 在秒改变时，更新 this.state.seconds
		if (seconds !== this.state.seconds) {
			var secondsShuffle = !this.state.secondsShuffle;
			this.setState({
				seconds: seconds,
				secondsShuffle: secondsShuffle
			});
		}
	};

	FlipClock.prototype.render = function render() {
		var _state = this.state;
		var hours = _state.hours;
		var minutes = _state.minutes;
		var seconds = _state.seconds;
		var hoursShuffle = _state.hoursShuffle;
		var minutesShuffle = _state.minutesShuffle;
		var secondsShuffle = _state.secondsShuffle;

		return React.createElement(
			'div',
			{ className: 'flipClock' },
			React.createElement(FlipUnitContainer, {
				unit: 'hours',
				digit: hours,
				shuffle: hoursShuffle
			}),
			React.createElement(FlipUnitContainer, {
				unit: 'minutes',
				digit: minutes,
				shuffle: minutesShuffle
			}),
			React.createElement(FlipUnitContainer, {
				unit: 'seconds',
				digit: seconds,
				shuffle: secondsShuffle
			})
		);
	};

	return FlipClock;
}(React.Component);

// 头部
var Header = function (_React$Component5) {
	_inherits(Header, _React$Component5);

	function Header() {
		_classCallCheck(this, Header);

		return _possibleConstructorReturn(this, _React$Component5.apply(this, arguments));
	}

	Header.prototype.render = function render() {
		return React.createElement(
			'header',
			null,
			React.createElement(
				'h1',
				null,
				' LEOPOLDO\'s'
			),
			React.createElement(
				'br',
			)
		);
	};

	return Header;
}(React.Component);

// App对象
var App = function (_React$Component6) {
	_inherits(App, _React$Component6);

	function App() {
		_classCallCheck(this, App);

		return _possibleConstructorReturn(this, _React$Component6.apply(this, arguments));
	}

	App.prototype.render = function render() {
		return React.createElement(
			'div',
			null,
			React.createElement(Header, null),
			React.createElement(FlipClock, null)
		);
	};

	return App;
}(React.Component);
